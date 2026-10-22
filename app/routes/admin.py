"""Trang quản trị /admin. Mọi route (trừ đăng nhập) cần quyền admin."""
import json

from flask import Blueprint, Response, abort, flash, g, redirect, render_template, request, url_for

from app.repositories import category_repo, order_repo, product_repo
from app.security import admin_required, login_user, safe_next
from app.services import admin_service, auth_service, order_service

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.context_processor
def admin_layout():
    return {"pending_orders": order_repo.count_by_status().get("pending", 0) if g.get("user") else 0,
            "statuses": order_service.STATUS_LABELS, "per_page_choices": admin_service.PER_PAGE_CHOICES}


@bp.route("/dang-nhap", methods=["GET", "POST"])
def login():
    next_url = safe_next(request.values.get("next"), url_for("admin.dashboard"))
    if g.user and g.user.get("is_admin"):
        return redirect(next_url)
    if request.method == "POST":
        user = auth_service.authenticate(request.form.get("phone", ""), request.form.get("password", ""))
        if user and user["is_admin"]:
            login_user(user["id"])
            return redirect(next_url)
        flash("Thông tin đăng nhập không đúng hoặc tài khoản không có quyền quản trị", "error")
    return render_template("admin/login.html", next=next_url, phone=request.form.get("phone", ""))


@bp.get("/")
@admin_required
def dashboard():
    data = admin_service.dashboard(admin_service.to_int(request.args.get("ky"), 30))
    inventory = admin_service.product_page(request.args.to_dict())
    return render_template("admin/dashboard.html", **data, inv=inventory)


# ---------- đơn hàng ----------

@bp.get("/don-hang")
@admin_required
def orders():
    return render_template("admin/orders.html", **admin_service.order_page(request.args))


@bp.route("/don-hang/<int:order_id>", methods=["GET", "POST"])
@admin_required
def order(order_id: int):
    o = order_repo.find_by_id(order_id)
    if o is None:
        abort(404)
    if request.method == "POST":
        try:
            admin_service.change_order_status(o, request.form.get("status", ""))
            flash("Đã cập nhật trạng thái đơn hàng", "success")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("admin.order", order_id=order_id))
    return render_template("admin/order.html", order=o, methods=order_service.PAYMENT_METHODS,
                           next_statuses=admin_service.TRANSITIONS[o["status"]])


@bp.get("/don-hang.csv")
@admin_required
def orders_csv():
    rows, _ = order_repo.admin_page(None, None, "id", True, 100_000, 0)
    body = admin_service.to_csv(
        ["Mã đơn", "Ngày", "Khách", "SĐT", "Địa chỉ", "Số SP", "Tổng tiền", "Thanh toán", "Trạng thái"],
        [[o["id"], o["created_at"], o["name"], o["phone"], o["address"], o["item_count"], o["total"],
          o["payment_method"], o["status"]] for o in rows])
    return Response(body, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=don-hang.csv"})


# ---------- sản phẩm ----------

@bp.get("/san-pham")
@admin_required
def products():
    return render_template("admin/products.html", **admin_service.product_page(request.args),
                           categories=category_repo.find_all())


@bp.get("/san-pham.csv")
@admin_required
def products_csv():
    rows, _ = product_repo.admin_page(None, None, None, admin_service.LOW_STOCK, "id", False, 100_000, 0)
    body = admin_service.to_csv(["ID", "Tên", "Hãng", "Danh mục", "Giá", "Giá gốc", "Tồn kho", "Đã bán"],
                                [[p["id"], p["name"], p["brand"], p["category_name"], p["price"], p["old_price"] or "",
                                  p["stock"], p["sold"]] for p in rows])
    return Response(body, mimetype="text/csv", headers={"Content-Disposition": "attachment; filename=san-pham.csv"})


def _product_form(product: dict | None):
    if request.method == "POST":
        try:
            if product is None:
                pid = admin_service.create_product(request.form, request.files)
                flash("Đã tạo sản phẩm", "success")
            else:
                admin_service.update_product(product, request.form, request.files)
                pid = product["id"]
                flash("Đã lưu thay đổi", "success")
            return redirect(url_for("admin.product_edit", product_id=pid))
        except ValueError as e:
            flash(str(e), "error")
    details = json.loads(product["details"]) if product else {}
    return render_template("admin/product_form.html", product=product, details=details, form=request.form,
                           categories=category_repo.find_all())


@bp.route("/san-pham/moi", methods=["GET", "POST"])
@admin_required
def product_new():
    return _product_form(None)


@bp.route("/san-pham/<int:product_id>", methods=["GET", "POST"])
@admin_required
def product_edit(product_id: int):
    product = product_repo.find_by_id(product_id)
    if product is None:
        abort(404)
    return _product_form(product)


@bp.post("/san-pham/<int:product_id>/xoa")
@admin_required
def product_delete(product_id: int):
    product = product_repo.find_by_id(product_id)
    if product is None:
        abort(404)
    try:
        admin_service.delete_product(product)
        flash(f"Đã xoá “{product['name']}”", "success")
        return redirect(url_for("admin.products"))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("admin.product_edit", product_id=product_id))


# ---------- danh mục, khách hàng ----------

@bp.get("/danh-muc")
@admin_required
def categories():
    return render_template("admin/categories.html", categories=category_repo.find_all())


@bp.route("/danh-muc/<int:category_id>", methods=["GET", "POST"])
@admin_required
def category_edit(category_id: int):
    category = category_repo.find_by_id(category_id)
    if category is None:
        abort(404)
    if request.method == "POST":
        try:
            admin_service.update_category(category, request.form)
            flash("Đã lưu danh mục", "success")
            return redirect(url_for("admin.categories"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("admin/category_form.html", category=category, form=request.form)


@bp.get("/khach-hang")
@admin_required
def customers():
    return render_template("admin/customers.html", **admin_service.customer_page(request.args))
