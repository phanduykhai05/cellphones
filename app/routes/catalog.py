"""Trang danh mục, tìm kiếm, chi tiết sản phẩm."""
from flask import Blueprint, abort, render_template, request

from app.repositories import content_repo
from app.services import catalog_service, product_service

bp = Blueprint("catalog", __name__)


def _filters() -> dict:
    """Đọc bộ lọc từ query string; giá trị lạ bị bỏ qua thay vì lỗi."""
    args = request.args
    f = {"brand": args.get("hang") or None, "q": args.get("q") or None,
         "sort": args.get("sap_xep", "popular"), "in_stock": args.get("con_hang") == "1"}
    price = args.get("gia", "")
    if price.isdigit() and int(price) < len(catalog_service.PRICE_RANGES):
        _, f["min_price"], f["max_price"] = catalog_service.PRICE_RANGES[int(price)]
    return f


def _active_filters() -> list[tuple[str, str]]:
    """(tham số, nhãn) của bộ lọc đang bật, để hiện chip có nút xoá."""
    active = [("hang", request.args["hang"])] if request.args.get("hang") else []
    price = request.args.get("gia", "")
    if price.isdigit() and int(price) < len(catalog_service.PRICE_RANGES):
        active.append(("gia", catalog_service.PRICE_RANGES[int(price)][0]))
    return active


def _render_listing(category: dict | None, title: str):
    filters = _filters()
    products = product_service.list_products(category_id=category["id"] if category else None, **filters)
    return render_template(
        "pages/category.html",
        category=category, title=title, products=products,
        brands=catalog_service.brands_with_logos(category["id"]) if category else [],
        needs=content_repo.quick_links(f"sub:{category['slug']}") if category else [],
        top_banners=content_repo.banners("plp"),
        price_ranges=catalog_service.PRICE_RANGES, sort_labels=catalog_service.SORT_LABELS,
        args=request.args, active_filters=_active_filters(),
    )


@bp.get("/danh-muc/<slug>")
def category(slug: str):
    cat = catalog_service.get_category(slug)
    if cat is None:
        abort(404)
    return _render_listing(cat, cat["short_name"])


@bp.get("/tim-kiem")
def search():
    q = request.args.get("q", "").strip()
    return _render_listing(None, f"Kết quả tìm kiếm “{q}”" if q else "Tất cả sản phẩm")


@bp.get("/san-pham/<slug>")
def product(slug: str):
    p = product_service.get_product_page(slug)
    if p is None:
        abort(404)
    return render_template("pages/product.html", product=p, related=product_service.related(p))
