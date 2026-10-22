"""Số liệu cho dashboard admin. days luôn là int (đã validate ở service) nên ghép vào modifier an toàn."""
from app.db import get_db

NOT_CANCELLED = "o.status != 'cancelled'"


def _window(days: int, offset: int = 0) -> tuple[str, str]:
    """Khoảng [now - (offset+days) ngày, now - offset ngày) dạng modifier của datetime() SQLite.
    Kỳ hiện tại (offset 0) lấy cận trên +1 ngày để không bỏ sót đơn vừa đặt trong cùng giây."""
    return f"-{offset + days} days", (f"-{offset} days" if offset else "+1 day")


def sales(days: int, offset: int = 0) -> dict:
    start, end = _window(days, offset)
    row = get_db().execute(
        "SELECT COALESCE(SUM(o.total), 0) AS revenue, COUNT(*) AS orders,"
        " COALESCE((SELECT SUM(oi.qty) FROM order_items oi JOIN orders o2 ON o2.id = oi.order_id"
        "   WHERE o2.status != 'cancelled' AND o2.created_at >= datetime('now', ?) AND o2.created_at < datetime('now', ?)), 0) AS units"
        f" FROM orders o WHERE {NOT_CANCELLED} AND o.created_at >= datetime('now', ?) AND o.created_at < datetime('now', ?)",
        (start, end, start, end)).fetchone()
    return dict(row)


def category_sales(days: int, offset: int = 0) -> list[dict]:
    """Mọi danh mục có sản phẩm, kèm số lượng bán + doanh thu trong khoảng (0 nếu chưa bán)."""
    start, end = _window(days, offset)
    rows = get_db().execute(
        "SELECT c.id, c.slug, c.short_name AS name,"
        " (SELECT image_url FROM products WHERE category_id = c.id AND image_url IS NOT NULL LIMIT 1) AS image,"
        " COALESCE(SUM(s.qty), 0) AS units, COALESCE(SUM(s.qty * s.price), 0) AS revenue"
        " FROM categories c"
        " LEFT JOIN (SELECT p.category_id, oi.qty, oi.price FROM order_items oi"
        "   JOIN orders o ON o.id = oi.order_id JOIN products p ON p.id = oi.product_id"
        f"   WHERE {NOT_CANCELLED} AND o.created_at >= datetime('now', ?) AND o.created_at < datetime('now', ?)) s"
        "   ON s.category_id = c.id"
        " WHERE EXISTS (SELECT 1 FROM products WHERE category_id = c.id)"
        " GROUP BY c.id ORDER BY revenue DESC, c.sort", (start, end)).fetchall()
    return [dict(r) for r in rows]
