"""Đặt hàng: validate thông tin giao hàng, tạo đơn từ giỏ."""
import re

from app.repositories import order_repo
from app.services import cart_service

PAYMENT_METHODS = {"cod": "Thanh toán khi nhận hàng (COD)", "bank": "Chuyển khoản ngân hàng"}
STATUS_LABELS = {"pending": "Chờ xác nhận", "paid": "Đã thanh toán", "shipping": "Đang giao",
                 "done": "Hoàn tất", "cancelled": "Đã huỷ"}


def place_order(user: dict, form: dict) -> int:
    name = (form.get("name") or "").strip()
    phone = re.sub(r"[\s.\-]", "", form.get("phone") or "")
    address = (form.get("address") or "").strip()
    note = (form.get("note") or "").strip()[:500]
    payment = form.get("payment")
    if not name or len(name) > 100:
        raise ValueError("Vui lòng nhập tên người nhận")
    if not re.fullmatch(r"0\d{9}", phone):
        raise ValueError("Số điện thoại người nhận không hợp lệ")
    if not 5 <= len(address) <= 255:
        raise ValueError("Vui lòng nhập địa chỉ nhận hàng")
    if payment not in PAYMENT_METHODS:
        raise ValueError("Vui lòng chọn phương thức thanh toán")
    lines = cart_service.lines()
    if not lines:
        raise ValueError("Giỏ hàng đang trống")
    items = [{"product_id": l["product"]["id"], "name": l["product"]["name"], "variant": l["variant"],
              "image_url": l["product"]["image_url"], "price": l["product"]["price"], "qty": l["qty"]} for l in lines]
    try:
        order_id = order_repo.insert(user["id"], name, phone, address, note, payment, items)
    except order_repo.OutOfStock as e:
        raise ValueError(f"“{e.args[0]}” không đủ hàng, vui lòng giảm số lượng") from None
    cart_service.clear()
    return order_id


def orders_of(user_id: int) -> list[dict]:
    return order_repo.find_by_user(user_id)


def get_order(order_id: int, user_id: int) -> dict | None:
    return order_repo.find_for_user(order_id, user_id)
