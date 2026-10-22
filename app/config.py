import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    """Mọi giá trị đọc từ biến môi trường (.env) — không hardcode."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev")
    DATABASE_PATH = str(BASE_DIR / os.environ.get("DATABASE_PATH", "instance/app.db"))
    # Thông tin cửa hàng hiển thị trên header/footer
    SITE_NAME = os.environ.get("SITE_NAME", "Cellphone")
    HOTLINE_SALES = os.environ.get("HOTLINE_SALES", "1800.0000")
    HOTLINE_COMPLAINT = os.environ.get("HOTLINE_COMPLAINT", "1800.0001")
    BANK_INFO = os.environ.get("BANK_INFO", "Ngân hàng ... - STK ... - Chủ TK ...")
    SESSION_COOKIE_HTTPONLY = True
    MAX_CONTENT_LENGTH = 6 * 1024 * 1024  # upload ảnh tối đa 5MB + phần form
    SESSION_COOKIE_SAMESITE = "Lax"
    COMPANY_INFO = os.environ.get("COMPANY_INFO", "Công ty của bạn - Địa chỉ - Mã số doanh nghiệp")
