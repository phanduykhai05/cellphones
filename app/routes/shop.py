"""Giỏ hàng, thanh toán, đơn hàng."""
from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.security import login_required, safe_next
from app.services import cart_service, order_service

bp = Blueprint("shop", __name__)


def _int(value, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


@bp.get("/gio-hang")
def cart():
    lines = cart_service.lines()
    return render_template("pages/cart.html", lines=lines, total=cart_service.total(lines))


@bp.post("/gio-hang/them")
def cart_add():
    try:
        cart_service.add(_int(request.form.get("product_id")), _int(request.form.get("qty"), 1),
                         request.form.get("color", ""))
    except ValueError as e:
        flash(str(e), "error")
        return redirect(safe_next(request.form.get("next"), url_for("shop.cart")))
    if request.form.get("buy_now"):
        return redirect(url_for("shop.checkout"))
    flash("Đã thêm sản phẩm vào giỏ hàng", "success")
    return redirect(url_for("shop.cart"))


@bp.post("/gio-hang/cap-nhat")
def cart_update():
    cart_service.update(request.form.get("key", ""), _int(request.form.get("qty"), 1))
    return redirect(url_for("shop.cart"))


@bp.post("/gio-hang/xoa")
def cart_remove():
    cart_service.remove(request.form.get("key", ""))
    return redirect(url_for("shop.cart"))


@bp.route("/thanh-toan", methods=["GET", "POST"])
@login_required
def checkout():
    lines = cart_service.lines()
    if not lines:
        flash("Giỏ hàng đang trống", "error")
        return redirect(url_for("shop.cart"))
    if request.method == "POST":
        try:
            order_id = order_service.place_order(g.user, request.form)
        except ValueError as e:
            flash(str(e), "error")
        else:
            return redirect(url_for("shop.order", order_id=order_id, moi=1))
    return render_template("pages/checkout.html", lines=lines, total=cart_service.total(lines),
                           methods=order_service.PAYMENT_METHODS, form=request.form)


@bp.get("/don-hang")
@login_required
def orders():
    return render_template("pages/orders.html", orders=order_service.orders_of(g.user["id"]),
                           statuses=order_service.STATUS_LABELS)


@bp.get("/don-hang/<int:order_id>")
@login_required
def order(order_id: int):
    o = order_service.get_order(order_id, g.user["id"])
    if o is None:
        abort(404)
    return render_template("pages/order.html", order=o, methods=order_service.PAYMENT_METHODS,
                           statuses=order_service.STATUS_LABELS, is_new=request.args.get("moi") == "1")
