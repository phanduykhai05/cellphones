import re

import pytest

from app import create_app
from app.db import get_db, init_db, seed

TOKEN = "test-csrf"


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE_PATH": str(tmp_path / "test.db")})
    with app.app_context():
        init_db()
        seed()
    return app


@pytest.fixture
def client(app):
    c = app.test_client()
    with c.session_transaction() as s:
        s["_csrf"] = TOKEN
    return c


def post(client, url, **data):
    r = client.post(url, data={"_csrf": TOKEN, **data})
    with client.session_transaction() as s:
        s["_csrf"] = TOKEN  # đăng nhập/đăng xuất tạo phiên mới (token mới) — trình duyệt thật nhận token ở trang kế tiếp
    return r


def product(app, slug="iphone-17-pro"):
    with app.app_context():
        return dict(get_db().execute("SELECT id, price, stock FROM products WHERE slug = ?", (slug,)).fetchone())


def register(client, phone="0912345678", password="secret123"):
    return post(client, "/dang-ky", name="Nguyễn Văn A", phone=phone, password=password, password2=password)


def test_csrf_required(client):
    assert client.post("/gio-hang/them", data={"product_id": 1}).status_code == 400
    assert client.post("/dang-nhap", data={"phone": "0912345678", "password": "x", "_csrf": "sai"}).status_code == 400


def test_register_login_logout(client):
    assert register(client).status_code == 302
    assert "Nguyễn Văn A" in client.get("/").get_data(as_text=True)
    assert register(client).status_code == 200  # trùng số điện thoại -> báo lỗi, không tạo
    post(client, "/dang-xuat")
    assert "Đăng nhập" in client.get("/").get_data(as_text=True)
    assert post(client, "/dang-nhap", phone="0912345678", password="sai-mat-khau").status_code == 200
    r = post(client, "/dang-nhap", phone="091 234 5678", password="secret123", next="/gio-hang")
    assert r.status_code == 302 and r.headers["Location"].endswith("/gio-hang")


def test_register_validation(client):
    assert post(client, "/dang-ky", name="A", phone="123", password="secret123", password2="secret123").status_code == 200
    assert post(client, "/dang-ky", name="A", phone="0912345678", password="123", password2="123").status_code == 200
    with client.application.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM users").fetchone()[0] == 0


def test_open_redirect_blocked(client):
    register(client)
    r = post(client, "/dang-nhap", phone="0912345678", password="secret123", next="//evil.com")
    assert r.headers["Location"] == "/"


def test_cart_add_update_remove(app, client):
    p = product(app)
    post(client, "/gio-hang/them", product_id=p["id"], color="Bạc")
    post(client, "/gio-hang/them", product_id=p["id"], color="Bạc")
    html = client.get("/gio-hang").get_data(as_text=True)
    assert "Màu: Bạc" in html and 'class="qty__value">2<' in html
    key = f"{p['id']}|Bạc"
    post(client, "/gio-hang/cap-nhat", key=key, qty=99)  # vượt giới hạn -> chặn ở min(10, tồn kho)
    with client.session_transaction() as s:
        assert s["cart"][key] == min(10, p["stock"])
    post(client, "/gio-hang/xoa", key=key)
    assert "đang trống" in client.get("/gio-hang").get_data(as_text=True)


def test_checkout_requires_login(app, client):
    post(client, "/gio-hang/them", product_id=product(app)["id"])
    r = client.get("/thanh-toan")
    assert r.status_code == 302 and "/dang-nhap" in r.headers["Location"]


def test_checkout_creates_order_and_decrements_stock(app, client):
    p = product(app)
    register(client)
    post(client, "/gio-hang/them", product_id=p["id"], qty=2, buy_now=1)
    r = post(client, "/thanh-toan", name="Người nhận", phone="0987654321", address="123 Lê Lợi, Q1, HCM", payment="bank")
    assert r.status_code == 302
    order_id = int(re.search(r"/don-hang/(\d+)", r.headers["Location"]).group(1))
    html = client.get(f"/don-hang/{order_id}?moi=1").get_data(as_text=True)
    assert "Đặt hàng thành công" in html and "Thông tin chuyển khoản" in html
    assert product(app)["stock"] == p["stock"] - 2
    with client.application.app_context():
        assert get_db().execute("SELECT total FROM orders WHERE id = ?", (order_id,)).fetchone()[0] == p["price"] * 2
    assert "đang trống" in client.get("/gio-hang").get_data(as_text=True)


def test_checkout_out_of_stock_rolls_back(app, client):
    p = product(app)
    register(client)
    post(client, "/gio-hang/them", product_id=p["id"], qty=3)
    with app.app_context():  # người khác mua hết trong lúc mình đang ở trang thanh toán
        get_db().execute("UPDATE products SET stock = 1 WHERE id = ?", (p["id"],))
        get_db().commit()
    r = post(client, "/thanh-toan", name="A", phone="0987654321", address="123 Lê Lợi", payment="cod")
    assert r.status_code == 200 and "không đủ hàng" in r.get_data(as_text=True)
    assert product(app)["stock"] == 1
    with app.app_context():
        assert get_db().execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 0


def test_cannot_view_other_users_order(app, client):
    register(client)
    post(client, "/gio-hang/them", product_id=product(app)["id"])
    r = post(client, "/thanh-toan", name="A", phone="0987654321", address="123 Lê Lợi", payment="cod")
    order_url = r.headers["Location"].split("?")[0]
    other = app.test_client()
    with other.session_transaction() as s:
        s["_csrf"] = TOKEN
    register(other, phone="0900000000")
    assert other.get(order_url).status_code == 404


def test_price_comes_from_db(app, client):
    p = product(app)
    register(client)
    post(client, "/gio-hang/them", product_id=p["id"], price=1)  # trường price giả mạo bị bỏ qua
    post(client, "/thanh-toan", name="A", phone="0987654321", address="123 Lê Lợi", payment="cod")
    with app.app_context():
        assert get_db().execute("SELECT total FROM orders").fetchone()[0] == p["price"]
