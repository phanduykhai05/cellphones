"""Giỏ hàng lưu trong session: {"<product_id>|<màu>": số lượng}. Giá luôn đọc lại từ DB."""
from flask import session

from app.repositories import product_repo

MAX_QTY = 10  # giới hạn mỗi dòng, như các site TMĐT


def _cart() -> dict[str, int]:
    return session.setdefault("cart", {})


def _save() -> None:
    session.modified = True


def add(product_id: int, qty: int = 1, variant: str = "") -> None:
    product = product_repo.find_by_id(product_id)
    if product is None:
        raise ValueError("Sản phẩm không tồn tại")
    if product["stock"] <= 0:
        raise ValueError("Sản phẩm tạm hết hàng")
    key = f"{product_id}|{variant.strip()[:50]}"
    cart = _cart()
    cart[key] = min(cart.get(key, 0) + max(qty, 1), MAX_QTY, product["stock"])
    _save()


def update(key: str, qty: int) -> None:
    cart = _cart()
    if key not in cart:
        return
    if qty <= 0:
        cart.pop(key)
    else:
        product = product_repo.find_by_id(int(key.split("|")[0]))
        cart[key] = min(qty, MAX_QTY, product["stock"] if product else 0) or 1
    _save()


def remove(key: str) -> None:
    _cart().pop(key, None)
    _save()


def clear() -> None:
    session.pop("cart", None)


def count() -> int:
    return sum(session.get("cart", {}).values())


def lines() -> list[dict]:
    """Các dòng hàng kèm giá hiện tại từ DB; dòng của sản phẩm đã bị xoá thì bỏ qua."""
    result = []
    for key, qty in session.get("cart", {}).items():
        pid, _, variant = key.partition("|")
        product = product_repo.find_by_id(int(pid)) if pid.isdigit() else None
        if product:
            result.append({"key": key, "product": product, "variant": variant, "qty": qty,
                           "subtotal": product["price"] * qty, "in_stock": product["stock"] >= qty})
    return result


def total(items: list[dict]) -> int:
    return sum(line["subtotal"] for line in items)
