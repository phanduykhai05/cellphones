"""Nghiệp vụ trang quản trị: dashboard, phân trang, form sản phẩm/danh mục, trạng thái đơn, xuất CSV."""
import csv
import io
import json
import math
import re
import secrets
from pathlib import Path

from flask import current_app

from app.repositories import category_repo, order_repo, product_repo, stats_repo, user_repo
from app.services import order_service, product_service

LOW_STOCK = 5  # tồn kho <= 5 coi là "sắp hết"
PER_PAGE_CHOICES = (8, 20, 50)
PERIODS = (7, 30, 90)  # số ngày cho bộ chọn khoảng thời gian trên dashboard
IMAGE_TYPES = {".jpg", ".jpeg", ".png", ".webp"}
MAX_IMAGE_BYTES = 5 * 1024 * 1024

# Trạng thái đơn -> các trạng thái được phép chuyển sang (không cho mở lại đơn đã huỷ/hoàn tất)
TRANSITIONS = {
    "pending": ["paid", "shipping", "cancelled"],
    "paid": ["shipping", "cancelled"],
    "shipping": ["done", "cancelled"],
    "done": [],
    "cancelled": [],
}


# ---------- tiện ích chung ----------

def to_int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def paginate(fetch, page: int, per_page: int) -> dict:
    """fetch(limit, offset) -> (items, total). Trả dict để template vẽ footer bảng."""
    per_page = per_page if per_page in PER_PAGE_CHOICES else PER_PAGE_CHOICES[0]
    page = max(page, 1)
    items, total = fetch(per_page, (page - 1) * per_page)
    pages = max(math.ceil(total / per_page), 1)
    if page > pages and total:
        page = pages
        items, total = fetch(per_page, (page - 1) * per_page)
    start = (page - 1) * per_page + 1 if total else 0
    return {"items": items, "total": total, "page": page, "per_page": per_page, "pages": pages,
            "start": start, "end": start + len(items) - 1 if items else 0,
            "window": [p for p in range(1, pages + 1) if p <= 5 or abs(p - page) <= 1 or p == pages]}


def sort_args(args, allowed: dict, default: str) -> tuple[str, bool]:
    sort = args.get("sap_xep", default)
    return (sort if sort in allowed else default), args.get("chieu", "desc" if sort == default else "asc") == "desc"


def change(cur: float, prev: float) -> float | None:
    """% thay đổi so với kỳ trước; None khi kỳ trước = 0 (không chia được)."""
    return None if not prev else round((cur - prev) * 100 / prev, 1)


# ---------- dashboard ----------

def dashboard(days: int) -> dict:
    days = days if days in PERIODS else 30
    cur, prev = stats_repo.sales(days), stats_repo.sales(days, offset=days)
    aov = lambda s: s["revenue"] / s["orders"] if s["orders"] else 0  # noqa: E731
    kpis = [
        {"title": "Doanh thu", "value": cur["revenue"], "prev": prev["revenue"], "money": True},
        {"title": "Đơn hàng", "value": cur["orders"], "prev": prev["orders"]},
        {"title": "Giá trị đơn TB", "value": round(aov(cur)), "prev": round(aov(prev)), "money": True},
        {"title": "Sản phẩm đã bán", "value": cur["units"], "prev": prev["units"]},
    ]
    for k in kpis:
        k["change"] = change(k["value"], k["prev"])
    cats = stats_repo.category_sales(days)
    prev_rev = {c["id"]: c["revenue"] for c in stats_repo.category_sales(days, offset=days)}
    for c in cats:
        c["change"] = change(c["revenue"], prev_rev.get(c["id"], 0))
    max_units = max((c["units"] for c in cats), default=0)
    return {"days": days, "kpis": kpis, "categories": cats, "max_units": max_units,
            "units_change": kpis[3]["change"]}


# ---------- sản phẩm ----------

def stock_status(stock: int) -> str:
    return "out" if stock <= 0 else "low" if stock <= LOW_STOCK else "in"


def product_page(args) -> dict:
    sort, desc = sort_args(args, product_repo.ADMIN_SORTS, "id")
    stock = args.get("ton") if args.get("ton") in ("in", "low", "out") else None
    category = category_repo.find_by_slug(args.get("danh_muc", "")) if args.get("danh_muc") else None
    q = (args.get("q") or "").strip() or None
    page = paginate(lambda limit, offset: product_repo.admin_page(
        q, category["id"] if category else None, stock, LOW_STOCK, sort, desc, limit, offset),
        to_int(args.get("trang"), 1), to_int(args.get("so_dong"), PER_PAGE_CHOICES[0]))
    for p in page["items"]:
        p["stock_status"] = stock_status(p["stock"])
    return {"page": page, "sort": sort, "desc": desc, "stock": stock, "q": q, "category": category,
            "counts": product_repo.stock_counts(LOW_STOCK)}


def parse_specs(text: str) -> list[list[str]]:
    """Mỗi dòng "Nhãn: Giá trị" -> [nhãn, giá trị]; dòng không có ":" bị bỏ qua."""
    specs = []
    for line in (text or "").splitlines():
        label, sep, value = line.partition(":")
        if sep and label.strip() and value.strip():
            specs.append([label.strip()[:60], value.strip()[:500]])
    return specs[:40]


def save_image(file) -> str | None:
    """Lưu ảnh upload vào static/img/products/upload-<random>.<ext>; trả đường dẫn tương đối static."""
    if not file or not file.filename:
        return None
    ext = Path(file.filename).suffix.lower()
    if ext not in IMAGE_TYPES:
        raise ValueError("Ảnh phải là JPG, PNG hoặc WebP")
    data = file.read(MAX_IMAGE_BYTES + 1)
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("Ảnh tối đa 5MB")
    # Kiểm tra chữ ký file thật, không tin đuôi file
    if not (data[:3] == b"\xff\xd8\xff" or data[:8] == b"\x89PNG\r\n\x1a\n" or (data[:4] == b"RIFF" and data[8:12] == b"WEBP")):
        raise ValueError("File không phải ảnh hợp lệ")
    rel = f"img/products/upload-{secrets.token_hex(8)}{'.jpg' if ext == '.jpeg' else ext}"
    (Path(current_app.static_folder) / rel).write_bytes(data)
    return rel


def product_fields(form, files, existing: dict | None = None) -> dict:
    """Validate form sản phẩm -> dict cột để lưu. Lỗi -> ValueError."""
    name = (form.get("name") or "").strip()
    brand = (form.get("brand") or "").strip()
    if not name or len(name) > 200:
        raise ValueError("Tên sản phẩm bắt buộc (tối đa 200 ký tự)")
    if not brand or len(brand) > 60:
        raise ValueError("Hãng bắt buộc (tối đa 60 ký tự)")
    category = category_repo.find_by_id(to_int(form.get("category_id")))
    if category is None:
        raise ValueError("Vui lòng chọn danh mục")
    price, stock = to_int(form.get("price"), -1), to_int(form.get("stock"), -1)
    old_price = to_int(form.get("old_price"), -1) if form.get("old_price") else None
    if price < 0 or stock < 0:
        raise ValueError("Giá và tồn kho phải là số nguyên không âm")
    if old_price is not None and old_price < price:
        raise ValueError("Giá gốc phải lớn hơn hoặc bằng giá bán")
    details = json.loads(existing["details"]) if existing else {}
    details["specs"] = parse_specs(form.get("specs"))
    fields = {"name": name, "brand": brand, "category_id": category["id"], "price": price, "old_price": old_price,
              "stock": stock, "promo": (form.get("promo") or "").strip()[:300] or None,
              "details": json.dumps(details, ensure_ascii=False)}
    image = save_image(files.get("image"))
    if image:
        fields["image_url"] = image
    return fields


def create_product(form, files) -> int:
    fields = product_fields(form, files)
    pid = product_service.create_product({"name": fields["name"], "brand": fields["brand"], "price": fields["price"],
                                          "old_price": fields["old_price"], "stock": fields["stock"],
                                          "category": category_repo.find_by_id(fields["category_id"])["slug"]})
    product_repo.update(pid, fields)
    return pid


def update_product(product: dict, form, files) -> None:
    fields = product_fields(form, files, product)
    slug = product_service.slugify(fields["name"])
    other = product_repo.find_by_slug(slug)
    if other and other["id"] != product["id"]:
        raise ValueError("Đã có sản phẩm khác cùng tên")
    fields["slug"] = slug
    product_repo.update(product["id"], fields)


def delete_product(product: dict) -> None:
    if product_repo.has_orders(product["id"]):
        raise ValueError("Sản phẩm đã có trong đơn hàng nên không xoá được — hãy đặt tồn kho = 0 để ngừng bán")
    product_repo.delete(product["id"])


# ---------- danh mục ----------

def update_category(category: dict, form) -> None:
    name, short = (form.get("name") or "").strip(), (form.get("short_name") or "").strip()
    if not name or not short or len(name) > 60 or len(short) > 40:
        raise ValueError("Tên và tên ngắn bắt buộc (tối đa 60/40 ký tự)")
    category_repo.update(category["id"], name, short, max(to_int(form.get("home_group")), 0), to_int(form.get("sort")))


# ---------- đơn hàng ----------

def order_page(args) -> dict:
    sort, desc = sort_args(args, order_repo.ADMIN_SORTS, "id")
    status = args.get("trang_thai") if args.get("trang_thai") in order_service.STATUS_LABELS else None
    q = (args.get("q") or "").strip() or None
    page = paginate(lambda limit, offset: order_repo.admin_page(q, status, sort, desc, limit, offset),
                    to_int(args.get("trang"), 1), to_int(args.get("so_dong"), PER_PAGE_CHOICES[0]))
    return {"page": page, "sort": sort, "desc": desc, "status": status, "q": q, "counts": order_repo.count_by_status()}


def change_order_status(order: dict, new_status: str) -> None:
    if new_status not in TRANSITIONS.get(order["status"], []):
        raise ValueError("Không thể chuyển sang trạng thái này")
    order_repo.update_status(order["id"], new_status, restock=new_status == "cancelled")


# ---------- khách hàng ----------

def customer_page(args) -> dict:
    q = (args.get("q") or "").strip() or None
    page = paginate(lambda limit, offset: user_repo.admin_page(q, limit, offset),
                    to_int(args.get("trang"), 1), to_int(args.get("so_dong"), PER_PAGE_CHOICES[0]))
    return {"page": page, "q": q}


# ---------- CSV ----------

def to_csv(header: list[str], rows: list[list]) -> str:
    """CSV có BOM để Excel mở tiếng Việt đúng; chặn CSV injection (ô bắt đầu bằng = + - @ tab, CR)."""
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerow(header)
    for row in rows:
        writer.writerow(["'" + v if isinstance(v, str) and re.match(r"[=+\-@\t\r]", v) else v for v in row])
    return "﻿" + buf.getvalue()
