"""Ghép dữ liệu cho các trang: danh mục, mega menu, block trang chủ."""
from itertools import groupby

from app.repositories import category_repo, content_repo, product_repo
from app.services import product_service

PRICE_RANGES = [  # (nhãn, min, max) — max không tính
    ("Dưới 2 triệu", None, 2_000_000), ("Từ 2 - 4 triệu", 2_000_000, 4_000_000),
    ("Từ 4 - 7 triệu", 4_000_000, 7_000_000), ("Từ 7 - 13 triệu", 7_000_000, 13_000_000),
    ("Từ 13 - 20 triệu", 13_000_000, 20_000_000), ("Trên 20 triệu", 20_000_000, None),
]
SORT_LABELS = [("popular", "Phổ biến"), ("discount", "Khuyến mãi HOT"),
               ("price_asc", "Giá Thấp - Cao"), ("price_desc", "Giá Cao - Thấp")]


def categories() -> list[dict]:
    return category_repo.find_all()


def get_category(slug: str) -> dict | None:
    return category_repo.find_by_slug(slug)


def brands_with_logos(category_id: int) -> list[dict]:
    logos = content_repo.brand_logos()
    return [{"name": b, "logo": logos.get(b)} for b in product_repo.brands_in_category(category_id)]


def mega_menus() -> dict[str, dict]:
    """Nội dung mega menu cho từng danh mục có sản phẩm."""
    menus = {}
    for c in categories():
        if c["product_count"]:
            menus[c["slug"]] = {
                "brands": brands_with_logos(c["id"]),
                "hot": product_repo.find_all(category_id=c["id"], sort="discount", limit=12),
            }
    return menus


def home_blocks() -> list[dict]:
    """Mỗi nhóm home_group thành 1 block: banner trái + các tab danh mục."""
    cats = [c for c in categories() if c["home_group"] and c["product_count"]]
    blocks = []
    for _, group in groupby(sorted(cats, key=lambda c: (c["home_group"], c["sort"])), key=lambda c: c["home_group"]):
        tabs = [{"category": c,
                 "links": content_repo.quick_links(f"sub:{c['slug']}"),
                 "brands": product_repo.brands_in_category(c["id"])[:10],
                 "products": product_service.list_products(category_id=c["id"], limit=16)} for c in group]
        blocks.append({"banner": next((t["category"]["banner"] for t in tabs if t["category"]["banner"]), None),
                       "tabs": tabs})
    return blocks


def deal_tabs() -> list[dict]:
    images = content_repo.banners("deal_tab")
    sets = [("discount", "Deal sốc mỗi ngày"), ("popular", "Sản phẩm hot trend"), ("newest", "Hàng mới về")]
    return [{"title": title, "image": images[i]["image"] if i < len(images) else None,
             "products": product_service.list_products(sort=sort, limit=10)} for i, (sort, title) in enumerate(sets)]
