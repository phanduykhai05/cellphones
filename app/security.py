"""CSRF, người dùng hiện tại, login_required."""
import secrets
from functools import wraps

from flask import abort, g, redirect, request, session, url_for

from app.repositories import user_repo

CSRF_EXEMPT_BLUEPRINTS = {"products"}  # JSON API: trình duyệt không gửi JSON cross-site nếu không qua CORS


def csrf_token() -> str:
    if "_csrf" not in session:
        session["_csrf"] = secrets.token_urlsafe(32)
    return session["_csrf"]


def check_csrf() -> None:
    if request.method == "POST" and request.blueprint not in CSRF_EXEMPT_BLUEPRINTS:
        sent = request.form.get("_csrf", "")
        if not secrets.compare_digest(sent, session.get("_csrf", "")) or not sent:
            abort(400, "Phiên làm việc hết hạn, vui lòng tải lại trang.")


def load_user() -> None:
    uid = session.get("user_id")
    g.user = user_repo.find_by_id(uid) if uid else None


def login_user(user_id: int) -> None:
    """Tạo phiên mới khi đăng nhập (chống session fixation) nhưng giữ giỏ hàng."""
    cart = session.get("cart", {})
    session.clear()
    session["cart"] = cart
    session["user_id"] = user_id


def logout_user() -> None:
    cart = session.get("cart", {})
    session.clear()
    session["cart"] = cart


def safe_next(target: str | None, default: str) -> str:
    """Chỉ cho redirect về đường dẫn nội bộ (chống open redirect)."""
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    return default


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login", next=request.full_path.rstrip("?")))
        return view(*args, **kwargs)
    return wrapped
