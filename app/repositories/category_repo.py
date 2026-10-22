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


def find_by_id(category_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
    return dict(row) if row else None


def update(category_id: int, name: str, short_name: str, home_group: int, sort: int) -> None:
    db = get_db()
    db.execute("UPDATE categories SET name = ?, short_name = ?, home_group = ?, sort = ? WHERE id = ?",
               (name, short_name, home_group, sort, category_id))
    db.commit()
