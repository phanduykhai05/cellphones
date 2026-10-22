import io
import re

import pytest

from app import create_app
from app.db import get_db, init_db, seed
from app.repositories import user_repo
from app.services import auth_service

TOKEN = "test-csrf"


@pytest.fixture
def app(tmp_path):
    app = create_app({"TESTING": True, "DATABASE_PATH": str(tmp_path / "test.db")})
    with app.app_context():
        init_db()
        seed()
        admin_id = auth_service.register("Quản Trị", "0900000001", "admin123")
        user_repo.set_admin(admin_id, True)
        auth_service.register("Khách Hàng", "0900000002", "khach123")
    return app


def client_for(app, phone=None, password=None):
    c = app.test_client()
    with c.session_transaction() as s:
        s["_csrf"] = TOKEN
    if phone:
        post(c, "/admin/dang-nhap", phone=phone, password=password)
    return c


def post(c, url, data=None, **kw):
    r = c.post(url, data={"_csrf": TOKEN, **(data or {}), **kw})
    with c.session_transaction() as s:
        s["_csrf"] = TOKEN
    return r


@pytest.fixture
def admin(app):
    return client_for(app, "0900000001", "admin123")


def q(app, sql, *args):
    with app.app_context():
        return get_db().execute(sql, args).fetchone()


def place_order(app, qty=2):
    """Khách đặt 1 đơn iPhone 17 Pro qua luồng thật; trả về (order_id, product_id)."""
    c = client_for(app)
    post(c, "/dang-nhap", phone="0900000002", password="khach123")
    pid = q(app, "SELECT id FROM products WHERE slug = 'iphone-17-pro'")[0]
    post(c, "/gio-hang/them", product_id=pid, qty=qty)
    r = post(c, "/thanh-toan", name="Khách Hàng", phone="0900000002", address="1 Lê Lợi, Q1", payment="cod")
    return int(re.search(r"/don-hang/(\d+)", r.headers["Location"]).group(1)), pid


def test_admin_requires_admin_role(app):
    anon = app.test_client()
    r = anon.get("/admin/")
    assert r.status_code == 302 and "/admin/dang-nhap" in r.headers["Location"]
    customer = client_for(app)
    post(customer, "/dang-nhap", phone="0900000002", password="khach123")
    assert customer.get("/admin/").status_code == 403
    # Trang đăng nhập admin từ chối tài khoản không phải admin
    c = client_for(app, "0900000002", "khach123")
    assert c.get("/admin/").status_code == 302


def test_create_admin_cli(app):
    runner = app.test_cli_runner()
    r = runner.invoke(args=["create-admin", "--phone", "0900000002", "--password", ""])
    assert r.exit_code == 0, r.output
    with app.app_context():
        assert user_repo.find_by_phone("0900000002")["is_admin"] == 1


def test_all_pages_render(app, admin):
    order_id, pid = place_order(app)
    for url in ["/admin/", "/admin/?ky=7&ton=low", "/admin/don-hang", "/admin/don-hang?trang_thai=pending&q=Khách",
                f"/admin/don-hang/{order_id}", "/admin/san-pham", "/admin/san-pham?sap_xep=price&chieu=asc&so_dong=20",
                "/admin/san-pham/moi", f"/admin/san-pham/{pid}", "/admin/danh-muc", "/admin/danh-muc/1", "/admin/khach-hang"]:
        assert admin.get(url).status_code == 200, url
    # Tham số lạ: bỏ qua, không lỗi
    assert admin.get("/admin/san-pham?sap_xep=drop&chieu=x&trang=-5&so_dong=999&ton=abc").status_code == 200
    html = admin.get("/admin/").get_data(as_text=True)
    assert "1 chờ xử lý" in html


def test_dashboard_counts_sales(app, admin):
    place_order(app, qty=2)
    html = admin.get("/admin/").get_data(as_text=True)
    price = q(app, "SELECT price FROM products WHERE slug = 'iphone-17-pro'")[0]
    assert f"{price * 2:,}".replace(",", ".") + "đ" in html  # doanh thu
    assert '--h: 100.0%' in html  # cột danh mục điện thoại cao nhất


def test_order_status_flow_and_restock(app, admin):
    order_id, pid = place_order(app, qty=2)
    stock_after_order = q(app, "SELECT stock FROM products WHERE id = ?", pid)[0]
    post(admin, f"/admin/don-hang/{order_id}", status="done")  # pending -> done không hợp lệ
    assert q(app, "SELECT status FROM orders WHERE id = ?", order_id)[0] == "pending"
    post(admin, f"/admin/don-hang/{order_id}", status="cancelled")
    assert q(app, "SELECT status FROM orders WHERE id = ?", order_id)[0] == "cancelled"
    assert q(app, "SELECT stock FROM products WHERE id = ?", pid)[0] == stock_after_order + 2
    post(admin, f"/admin/don-hang/{order_id}", status="paid")  # đơn đã huỷ không mở lại
    assert q(app, "SELECT status FROM orders WHERE id = ?", order_id)[0] == "cancelled"


def test_product_crud(app, admin):
    cat_id = q(app, "SELECT id FROM categories WHERE slug = 'laptop'")[0]
    r = post(admin, "/admin/san-pham/moi", name="Laptop Thử Nghiệm X1", brand="TestBrand", category_id=cat_id,
             price=10000000, old_price=12000000, stock=3, specs="CPU: Intel i5\nRAM: 16GB\ndòng rác")
    assert r.status_code == 302
    pid = int(r.headers["Location"].rstrip("/").split("/")[-1])
    row = q(app, "SELECT slug, details, stock FROM products WHERE id = ?", pid)
    assert row[0] == "laptop-thu-nghiem-x1" and '"CPU", "Intel i5"' in row[1] and row[2] == 3
    post(admin, f"/admin/san-pham/{pid}", name="Laptop Thử Nghiệm X2", brand="TestBrand", category_id=cat_id,
         price=9000000, stock=0)
    assert tuple(q(app, "SELECT slug, price, old_price FROM products WHERE id = ?", pid)) == ("laptop-thu-nghiem-x2", 9000000, None)
    # Giá gốc nhỏ hơn giá bán -> lỗi, không lưu
    post(admin, f"/admin/san-pham/{pid}", name="X", brand="B", category_id=cat_id, price=100, old_price=50, stock=1)
    assert q(app, "SELECT price FROM products WHERE id = ?", pid)[0] == 9000000
    post(admin, f"/admin/san-pham/{pid}/xoa")
    assert q(app, "SELECT COUNT(*) FROM products WHERE id = ?", pid)[0] == 0


def test_cannot_delete_ordered_product(app, admin):
    _, pid = place_order(app)
    post(admin, f"/admin/san-pham/{pid}/xoa")
    assert q(app, "SELECT COUNT(*) FROM products WHERE id = ?", pid)[0] == 1


def test_image_upload_rejects_fake_image(app, admin):
    pid = q(app, "SELECT id, name, brand, category_id, price, stock FROM products LIMIT 1")
    data = {"_csrf": TOKEN, "name": pid[1], "brand": pid[2], "category_id": pid[3], "price": pid[4], "stock": pid[5],
            "image": (io.BytesIO(b"<?php echo 1; ?>"), "shell.png")}
    r = admin.post(f"/admin/san-pham/{pid[0]}", data=data, content_type="multipart/form-data")
    assert "không phải ảnh hợp lệ" in r.get_data(as_text=True)


def test_csv_export_escapes_formulas(app, admin):
    c = client_for(app)
    post(c, "/dang-nhap", phone="0900000002", password="khach123")
    pid = q(app, "SELECT id FROM products LIMIT 1")[0]
    post(c, "/gio-hang/them", product_id=pid)
    post(c, "/thanh-toan", name="=HYPERLINK(\"http://x\")", phone="0900000002", address="1 Lê Lợi, Q1", payment="cod")
    body = admin.get("/admin/don-hang.csv").get_data(as_text=True)
    assert "'=HYPERLINK" in body and body.startswith("﻿")
    assert admin.get("/admin/san-pham.csv").status_code == 200
