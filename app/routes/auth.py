"""Đăng ký, đăng nhập, đăng xuất."""
from flask import Blueprint, flash, g, redirect, render_template, request, url_for

from app.security import login_user, logout_user, safe_next
from app.services import auth_service

bp = Blueprint("auth", __name__)


@bp.route("/dang-nhap", methods=["GET", "POST"])
def login():
    next_url = safe_next(request.values.get("next"), url_for("main.home"))
    if g.user:
        return redirect(next_url)
    if request.method == "POST":
        user = auth_service.authenticate(request.form.get("phone", ""), request.form.get("password", ""))
        if user:
            login_user(user["id"])
            flash(f"Xin chào {user['name']}!", "success")
            return redirect(next_url)
        flash("Số điện thoại hoặc mật khẩu không đúng", "error")
    return render_template("pages/auth.html", mode="login", next=next_url, form=request.form)


@bp.route("/dang-ky", methods=["GET", "POST"])
def register():
    next_url = safe_next(request.values.get("next"), url_for("main.home"))
    if request.method == "POST":
        f = request.form
        if f.get("password") != f.get("password2"):
            flash("Mật khẩu nhập lại không khớp", "error")
        else:
            try:
                user_id = auth_service.register(f.get("name"), f.get("phone"), f.get("password"), f.get("email"))
            except ValueError as e:
                flash(str(e), "error")
            else:
                login_user(user_id)
                flash("Đăng ký thành công!", "success")
                return redirect(next_url)
    return render_template("pages/auth.html", mode="register", next=next_url, form=request.form)


@bp.post("/dang-xuat")
def logout():
    logout_user()
    return redirect(url_for("main.home"))
