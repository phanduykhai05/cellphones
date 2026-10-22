"""JSON API cho sản phẩm. Route chỉ nhận request → gọi service → trả response."""
from flask import Blueprint, abort, jsonify, request

from app.services import product_service

bp = Blueprint("products", __name__, url_prefix="/api/products")


@bp.get("")
def list_products():
    return jsonify(product_service.list_products())


@bp.get("/<int:product_id>")
def get_product(product_id: int):
    product = product_service.get_product(product_id)
    if product is None:
        abort(404)
    return jsonify(product)


@bp.post("")
def create_product():
    try:
        new_id = product_service.create_product(request.get_json(silent=True) or {})
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(id=new_id), 201
