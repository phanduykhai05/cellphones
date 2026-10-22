"""Tầng truy cập dữ liệu: chỉ SQL, không có logic nghiệp vụ."""
from app.db import get_db

SORTS = {  # khoá sort hợp lệ -> ORDER BY (whitelist vì không bind được bằng ?)
    "popular": "p.id",
    "discount": "(COALESCE(p.old_price, p.price) - p.price) * 1.0 / COALESCE(p.old_price, p.price) DESC, p.id",
    "price_asc": "p.price, p.id",
    "price_desc": "p.price DESC, p.id",
    "newest": "p.id DESC",
}


def find_all(category_id: int | None = None, brand: str | None = None, q: str | None = None,
             min_price: int | None = None, max_price: int | None = None, in_stock: bool = False,
             sort: str = "popular", limit: int | None = None, exclude_id: int | None = None) -> list[dict]:
    where, params = [], []
    for cond, value in (("p.category_id = ?", category_id), ("p.brand = ?", brand), ("p.price >= ?", min_price),
                        ("p.price < ?", max_price), ("p.id != ?", exclude_id)):
        if value is not None:
            where.append(cond)
            params.append(value)
    if q:
        where.append("p.name LIKE ?")
        params.append(f"%{q}%")
    if in_stock:
        where.append("p.stock > 0")
    sql = "SELECT p.*, c.slug AS category_slug FROM products p JOIN categories c ON c.id = p.category_id"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY " + SORTS[sort]
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return [dict(r) for r in get_db().execute(sql, params).fetchall()]


def brands_in_category(category_id: int) -> list[str]:
    rows = get_db().execute(
        "SELECT brand FROM products WHERE category_id = ? GROUP BY brand ORDER BY COUNT(*) DESC, brand",
        (category_id,)).fetchall()
    return [r[0] for r in rows]


def find_by_id(product_id: int) -> dict | None:
    row = get_db().execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    return dict(row) if row else None


def find_by_slug(slug: str) -> dict | None:
    row = get_db().execute(
        "SELECT p.*, c.slug AS category_slug, c.name AS category_name FROM products p"
        " JOIN categories c ON c.id = p.category_id WHERE p.slug = ?", (slug,)).fetchone()
    return dict(row) if row else None


def insert(slug: str, name: str, brand: str, category_id: int, price: int, old_price: int | None, stock: int) -> int:
    db = get_db()
    cur = db.execute(
        "INSERT INTO products (slug, name, brand, category_id, price, old_price, stock) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (slug, name, brand, category_id, price, old_price, stock),
    )
    db.commit()
    return cur.lastrowid
