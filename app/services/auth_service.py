"""Đăng ký / đăng nhập: validate + băm mật khẩu."""
import re

from werkzeug.security import check_password_hash, generate_password_hash

from app.repositories import user_repo

PHONE_RE = re.compile(r"0\d{9}")
EMAIL_RE = re.compile(r"[^@\s]+@[^@\s]+\.[^@\s]+")
# Hash giả để thời gian kiểm tra như nhau dù số điện thoại có tồn tại hay không (không lộ tài khoản)
_DUMMY_HASH = generate_password_hash("dummy-password")


def normalize_phone(phone: str) -> str:
    return re.sub(r"[\s.\-]", "", phone or "")


def register(name: str, phone: str, password: str, email: str = "") -> int:
    name, phone, email = (name or "").strip(), normalize_phone(phone), (email or "").strip()
    if not name or len(name) > 100:
        raise ValueError("Vui lòng nhập họ tên (tối đa 100 ký tự)")
    if not PHONE_RE.fullmatch(phone):
        raise ValueError("Số điện thoại phải gồm 10 chữ số, bắt đầu bằng 0")
    if email and not EMAIL_RE.fullmatch(email):
        raise ValueError("Email không hợp lệ")
    if not 6 <= len(password or "") <= 128:
        raise ValueError("Mật khẩu phải từ 6 đến 128 ký tự")
    if user_repo.find_by_phone(phone):
        raise ValueError("Số điện thoại đã được đăng ký")
    return user_repo.insert(name, phone, email or None, generate_password_hash(password))


def authenticate(phone: str, password: str) -> dict | None:
    user = user_repo.find_by_phone(normalize_phone(phone))
    if user is None:
        check_password_hash(_DUMMY_HASH, password or "")
        return None
    return user if check_password_hash(user["password_hash"], password or "") else None
