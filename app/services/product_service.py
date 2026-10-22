"""Tầng nghiệp vụ: validate, xử lý dữ liệu, gọi repository."""
import json
import re
import unicodedata

from app.repositories import category_repo, product_repo


def _decorate(p: dict) -> dict:
    old = p["old_price"]
    p["discount"] = round((old - p["price"]) * 100 / old) if old else 0
    # ponytail: ưu đãi thành viên = 1% giá (quan sát từ site gốc), thay bằng bảng khuyến mãi khi có
    p["member_discount"] = p["price"] // 100 // 1000 * 1000
    p["tags"] = re.findall(r"\b\d+\s?(?:GB|TB)\b", p["name"])[-2:]
    return p


def list_products(**filters) -> list[dict]:
    if filters.get("q"):
        filters["q"] = filters["q"].strip() or None
    if filters.get("sort") not in product_repo.SORTS:
        filters["sort"] = "popular"
    return [_decorate(p) for p in product_repo.find_all(**filters)]


def get_product(product_id: int) -> dict | None:
    return product_repo.find_by_id(product_id)


def get_product_page(slug: str) -> dict | None:
    p = product_repo.find_by_slug(slug)
    if p is None:
        return None
    p = _decorate(p)
    p["details"] = json.loads(p["details"])
    p["details"].setdefault("gallery", [])
    if not p["details"]["gallery"] and p["image_url"]:
        p["details"]["gallery"] = [p["image_url"]]
    p["installment"] = p["price"] // 10 // 1000 * 1000  # trả góp 10 tháng, làm tròn nghìn
    return p


def related(product: dict, limit: int = 10) -> list[dict]:
    return list_products(category_id=product["category_id"], exclude_id=product["id"], limit=limit)


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]+", "-", text.encode("ascii", "ignore").decode().lower()).strip("-")


def create_product(data: dict) -> int:
    name = (data.get("name") or "").strip()
    brand = (data.get("brand") or "").strip()
    if not name or not brand:
        raise ValueError("Tên và hãng không được để trống")
    category = category_repo.find_by_slug(data.get("category") or "dien-thoai")
    if category is None:
        raise ValueError("Danh mục không tồn tại")
    try:
        price = int(data.get("price", 0))
        stock = int(data.get("stock", 0))
        old_price = int(data["old_price"]) if data.get("old_price") is not None else None
    except (TypeError, ValueError):
        raise ValueError("Giá và tồn kho phải là số nguyên")
    if price < 0 or stock < 0:
        raise ValueError("Giá và tồn kho không được âm")
    if old_price is not None and old_price < price:
        raise ValueError("Giá gốc phải lớn hơn hoặc bằng giá bán")
    slug = slugify(name)
    if product_repo.find_by_slug(slug):
        raise ValueError("Sản phẩm đã tồn tại")
    return product_repo.insert(slug, name, brand, category["id"], price, old_price, stock)
