"""Tầng truy cập dữ liệu: chỉ SQL, không có logic nghiệp vụ."""
from app.db import get_db


def find_by_id(user_id: int) -> dict | None:
    row = get_db().execute("SELECT id, name, phone, email FROM users WHERE id = ?", (user_id,)).fetchone()
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
