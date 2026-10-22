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


ADMIN_SORTS = {"name": "p.name", "category": "c.short_name", "price": "p.price", "stock": "p.stock", "id": "p.id"}


def admin_page(q: str | None, category_id: int | None, stock: str | None, low: int, sort: str, desc: bool,
               limit: int, offset: int) -> tuple[list[dict], int]:
    """stock: None | 'in' (> low) | 'low' (1..low) | 'out' (0). sort phải thuộc ADMIN_SORTS."""
    where, params = [], []
    if q:
        where.append("(p.name LIKE ? OR p.brand LIKE ?)")
        params += [f"%{q}%"] * 2
    if category_id:
        where.append("p.category_id = ?")
        params.append(category_id)
    if stock == "in":
        where.append("p.stock > ?")
        params.append(low)
    elif stock == "low":
        where.append("p.stock BETWEEN 1 AND ?")
        params.append(low)
    elif stock == "out":
        where.append("p.stock = 0")
    sql_where = " WHERE " + " AND ".join(where) if where else ""
    db = get_db()
    total = db.execute(f"SELECT COUNT(*) FROM products p{sql_where}", params).fetchone()[0]
    order = f"{ADMIN_SORTS[sort]} {'DESC' if desc else 'ASC'}, p.id"
    rows = db.execute(
        "SELECT p.*, c.short_name AS category_name, c.slug AS category_slug,"
        " (SELECT COALESCE(SUM(oi.qty), 0) FROM order_items oi JOIN orders o ON o.id = oi.order_id"
        "  WHERE oi.product_id = p.id AND o.status != 'cancelled') AS sold"
        f" FROM products p JOIN categories c ON c.id = p.category_id{sql_where}"
        f" ORDER BY {order} LIMIT ? OFFSET ?", [*params, limit, offset]).fetchall()
    return [dict(r) for r in rows], total


def stock_counts(low: int) -> dict[str, int]:
    row = get_db().execute(
        "SELECT COUNT(*), SUM(stock > ?), SUM(stock BETWEEN 1 AND ?), SUM(stock = 0) FROM products",
        (low, low)).fetchone()
    return {"all": row[0], "in": row[1] or 0, "low": row[2] or 0, "out": row[3] or 0}


def update(product_id: int, fields: dict) -> None:
    """fields: chỉ các cột trong UPDATABLE."""
    cols = [c for c in fields if c in UPDATABLE]
    db = get_db()
    db.execute(f"UPDATE products SET {', '.join(f'{c} = ?' for c in cols)} WHERE id = ?",
               [fields[c] for c in cols] + [product_id])
    db.commit()


UPDATABLE = {"slug", "name", "brand", "category_id", "price", "old_price", "stock", "promo", "image_url", "details"}


def has_orders(product_id: int) -> bool:
    return get_db().execute("SELECT 1 FROM order_items WHERE product_id = ? LIMIT 1", (product_id,)).fetchone() is not None


def delete(product_id: int) -> None:
    db = get_db()
    db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
