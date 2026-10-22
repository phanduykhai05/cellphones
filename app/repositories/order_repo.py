"""Tầng truy cập dữ liệu: chỉ SQL, không có logic nghiệp vụ."""
from app.db import get_db


class OutOfStock(Exception):
    """Một dòng hàng không đủ tồn kho; args[0] là tên sản phẩm."""


def insert(user_id: int, name: str, phone: str, address: str, note: str, payment: str, items: list[dict]) -> int:
    """Tạo đơn + trừ kho trong 1 transaction. items: product_id, name, variant, image_url, price, qty."""
    db = get_db()
    try:
        for it in items:
            # Điều kiện stock >= qty nằm trong chính câu UPDATE: 2 đơn đặt cùng lúc không thể cùng trừ quá kho
            cur = db.execute("UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
                             (it["qty"], it["product_id"], it["qty"]))
            if cur.rowcount == 0:
                raise OutOfStock(it["name"])
        total = sum(it["price"] * it["qty"] for it in items)
        order_id = db.execute(
            "INSERT INTO orders (user_id, name, phone, address, note, payment_method, total) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (user_id, name, phone, address, note, payment, total)).lastrowid
        db.executemany(
            "INSERT INTO order_items (order_id, product_id, name, variant, image_url, price, qty)"
            " VALUES (:order_id, :product_id, :name, :variant, :image_url, :price, :qty)",
            [{**it, "order_id": order_id} for it in items])
        db.commit()
        return order_id
    except Exception:
        db.rollback()
        raise


def find_by_user(user_id: int) -> list[dict]:
    rows = get_db().execute(
        "SELECT o.*, (SELECT SUM(qty) FROM order_items WHERE order_id = o.id) AS item_count"
        " FROM orders o WHERE user_id = ? ORDER BY id DESC", (user_id,)).fetchall()
    return [dict(r) for r in rows]


def find_for_user(order_id: int, user_id: int) -> dict | None:
    """Chỉ trả đơn thuộc về user này (không cho xem đơn người khác bằng cách đoán id)."""
    db = get_db()
    row = db.execute("SELECT * FROM orders WHERE id = ? AND user_id = ?", (order_id, user_id)).fetchone()
    if row is None:
        return None
    order = dict(row)
    order["items"] = [dict(r) for r in db.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))]
    return order
