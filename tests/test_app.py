import re

import pytest

from app import create_app
from app.db import init_db, seed


@pytest.fixture
def client(tmp_path):
    app = create_app({"TESTING": True, "DATABASE_PATH": str(tmp_path / "test.db")})
    with app.app_context():
        init_db()
        seed()
    return app.test_client()


def cards(html: str) -> list[str]:
    """Tên sản phẩm trong các card (mega menu ở header cũng chứa tên nên không so cả trang)."""
    return re.findall(r'class="pc__name">([^<]+)<', html)


def test_pages_render(client):
    home = client.get("/").get_data(as_text=True)
    assert "iPhone 17 Pro 256GB" in home and "31.990.000đ" in home
    assert client.get("/danh-muc/dien-thoai").status_code == 200
    pdp = client.get("/san-pham/iphone-17-pro").get_data(as_text=True)
    assert "Chip A19 Pro" in pdp and "Cam Vũ Trụ" in pdp
    assert client.get("/danh-muc/khong-co").status_code == 404
    assert client.get("/san-pham/khong-co").status_code == 404


def test_category_filters(client):
    names = cards(client.get("/danh-muc/dien-thoai?hang=Samsung").get_data(as_text=True))
    assert names and all("Samsung" in n for n in names)
    # gia=0 là "Dưới 2 triệu": không có điện thoại nào
    assert "Không tìm thấy" in client.get("/danh-muc/dien-thoai?gia=0").get_data(as_text=True)
    asc = client.get("/danh-muc/laptop?sap_xep=price_asc").get_data(as_text=True)
    prices = [int(p.replace(".", "")) for p in re.findall(r"<strong>([\d.]+)đ</strong>", asc)]
    assert prices == sorted(prices)
    # tham số lạ bị bỏ qua, không lỗi
    assert client.get("/danh-muc/laptop?sap_xep=drop&gia=99").status_code == 200


def test_search(client):
    names = cards(client.get("/tim-kiem?q=macbook").get_data(as_text=True))
    assert names and all("MacBook" in n for n in names)


def test_api_create_and_validate(client):
    r = client.post("/api/products", json={"name": "Điện thoại Test X", "brand": "Test", "category": "dien-thoai",
                                           "price": 1000000, "old_price": 1500000, "stock": 1})
    assert r.status_code == 201
    assert client.get("/san-pham/dien-thoai-test-x").status_code == 200
    bad = [{"name": "", "brand": "X"}, {"name": "A", "brand": "B", "price": -1},
           {"name": "A", "brand": "B", "price": 10, "old_price": 5}, {"name": "A", "brand": "B", "category": "nope"}]
    for body in bad:
        assert client.post("/api/products", json=body).status_code == 400
