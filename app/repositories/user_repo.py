"""Tầng truy cập dữ liệu: chỉ SQL, không có logic nghiệp vụ."""
from app.db import get_db


def find_by_id(user_id: int) -> dict | None:
    row = get_db().execute("SELECT id, name, phone, email, is_admin FROM users WHERE id = ?", (user_id,)).fetchone()
    return dict(row) if row else None


def find_by_phone(phone: str) -> dict | None:
    row = get_db().execute("SELECT * FROM users WHERE phone = ?", (phone,)).fetchone()
    return dict(row) if row else None


def insert(name: str, phone: str, email: str | None, password_hash: str) -> int:
    db = get_db()
    cur = db.execute("INSERT INTO users (name, phone, email, password_hash) VALUES (?, ?, ?, ?)",
                     (name, phone, email, password_hash))
    db.commit()
    return cur.lastrowid


def set_admin(user_id: int, is_admin: bool) -> None:
    db = get_db()
    db.execute("UPDATE users SET is_admin = ? WHERE id = ?", (int(is_admin), user_id))
    db.commit()


def admin_page(q: str | None, limit: int, offset: int) -> tuple[list[dict], int]:
    where, params = "", []
    if q:
        where = "WHERE u.name LIKE ? OR u.phone LIKE ? OR u.email LIKE ?"
        params = [f"%{q}%"] * 3
    db = get_db()
    total = db.execute(f"SELECT COUNT(*) FROM users u {where}", params).fetchone()[0]
    rows = db.execute(
        "SELECT u.id, u.name, u.phone, u.email, u.is_admin, u.created_at,"
        " COUNT(o.id) AS order_count,"
        " COALESCE(SUM(CASE WHEN o.status != 'cancelled' THEN o.total END), 0) AS spent"
        f" FROM users u LEFT JOIN orders o ON o.user_id = u.id {where}"
        " GROUP BY u.id ORDER BY u.id DESC LIMIT ? OFFSET ?", [*params, limit, offset]).fetchall()
    return [dict(r) for r in rows], total
