"""Tầng truy cập dữ liệu: chỉ SQL, không có logic nghiệp vụ."""
from app.db import get_db


def find_all() -> list[dict]:
    rows = get_db().execute(
        "SELECT c.*, (SELECT COUNT(*) FROM products p WHERE p.category_id = c.id) AS product_count"
        " FROM categories c ORDER BY sort").fetchall()
    return [dict(r) for r in rows]


def find_by_slug(slug: str) -> dict | None:
    row = get_db().execute("SELECT * FROM categories WHERE slug = ?", (slug,)).fetchone()
    return dict(row) if row else None
