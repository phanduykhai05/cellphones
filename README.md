# Cellphonfake — Web bán điện thoại bằng Flask

Website thương mại điện tử bán điện thoại, laptop, đồng hồ, tivi, viết bằng **Flask + SQLite**, không dùng framework frontend.
Có hai phần:

- **Cửa hàng:** giao diện dựng theo cấu trúc của cellphones.com.vn. Gồm trang chủ, danh mục có bộ lọc, chi tiết sản phẩm, giỏ hàng, đặt hàng, tài khoản.
- **Trang quản trị `/admin`:** giao diện theo template Manifest Commerce (shadcn). Gồm tổng quan doanh thu, quản lý đơn hàng, sản phẩm, danh mục và khách hàng.

Dữ liệu mẫu có 101 sản phẩm thật (ảnh, giá, thông số), 12 danh mục và 34 banner. Có 24 test tự động.

> Ảnh chụp dưới đây dùng dữ liệu demo. Tên khách hàng và số điện thoại đều là dữ liệu giả.

---

## Cửa hàng

### Trang chủ

Header đỏ dính trên cùng, có dải khuyến mãi chạy chữ và thu gọn khi cuộn. Slider banner tự chuyển kèm thanh tab. Sidebar danh mục có mega menu khi rê chuột.

| Trang chủ | Mega menu danh mục |
|---|---|
| ![Trang chủ](docs/screenshots/shop-01-home.jpg) | ![Mega menu](docs/screenshots/shop-02-mega-menu.jpg) |

| Deal sốc / Hot trend / Hàng mới về | Khối sản phẩm theo danh mục |
|---|---|
| ![Deal](docs/screenshots/shop-03-home-deals.jpg) | ![Khối danh mục](docs/screenshots/shop-04-home-category-block.jpg) |

### Danh mục và chi tiết sản phẩm

Trang danh mục lọc được theo hãng, khoảng giá và tình trạng còn hàng, sắp xếp theo giá hoặc mức giảm. Hàng bộ lọc dính dưới header khi cuộn.
Trang chi tiết có gallery ảnh, chọn phiên bản và màu (đổi ảnh theo màu), khuyến mãi, bảng thông số, câu hỏi thường gặp và thanh mua cố định ở đáy.

| Danh mục | Chi tiết sản phẩm |
|---|---|
| ![Danh mục](docs/screenshots/shop-05-category.jpg) | ![Chi tiết](docs/screenshots/shop-06-product.jpg) |

### Giỏ hàng, tài khoản, đặt hàng

Khách chưa đăng nhập vẫn thêm được vào giỏ. Khi thanh toán, khách được yêu cầu đăng nhập hoặc đăng ký bằng số điện thoại, giỏ hàng không bị mất.
Thanh toán bằng COD hoặc chuyển khoản; đơn chuyển khoản hiện thông tin tài khoản ngân hàng và nội dung chuyển khoản.

| Giỏ hàng | Đăng nhập |
|---|---|
| ![Giỏ hàng](docs/screenshots/shop-07-cart.jpg) | ![Đăng nhập](docs/screenshots/shop-08-login.jpg) |

| Thông tin đặt hàng | Đặt hàng thành công |
|---|---|
| ![Thanh toán](docs/screenshots/shop-09-checkout.jpg) | ![Thành công](docs/screenshots/shop-10-order-success.jpg) |

| Đơn hàng của tôi |
|---|
| ![Đơn hàng của tôi](docs/screenshots/shop-11-my-orders.jpg) |

### Giao diện mobile

| Trang chủ | Chi tiết sản phẩm | Danh mục |
|---|---|---|
| ![Mobile trang chủ](docs/screenshots/shop-12-mobile-home.jpg) | ![Mobile chi tiết](docs/screenshots/shop-13-mobile-product.jpg) | ![Mobile danh mục](docs/screenshots/shop-14-mobile-category.jpg) |

---

## Trang quản trị `/admin`

Chỉ tài khoản có quyền quản trị mới vào được. Giao diện có hiệu ứng chuyển trang (View Transitions), số liệu chạy từ 0, biểu đồ mọc lên và bảng hiện dần từng dòng. Mọi hiệu ứng tự tắt khi máy bật chế độ giảm chuyển động.

### Tổng quan

Doanh thu, số đơn, giá trị đơn trung bình và số sản phẩm đã bán trong 7/30/90 ngày, kèm % so với kỳ trước. Biểu đồ số lượng bán theo danh mục, danh mục bán chạy và bảng tồn kho (còn hàng / sắp hết / hết hàng).

| Tổng quan | Tồn kho |
|---|---|
| ![Dashboard](docs/screenshots/admin-02-dashboard.jpg) | ![Tồn kho](docs/screenshots/admin-03-dashboard-inventory.jpg) |

### Đơn hàng

Tìm theo mã đơn, tên hoặc số điện thoại, lọc theo trạng thái, sắp xếp, phân trang và xuất CSV. Trạng thái đơn đổi theo đúng thứ tự; huỷ đơn thì hàng tự trả về kho.

| Danh sách đơn | Chi tiết đơn |
|---|---|
| ![Đơn hàng](docs/screenshots/admin-04-orders.jpg) | ![Chi tiết đơn](docs/screenshots/admin-05-order-detail.jpg) |

### Sản phẩm, danh mục, khách hàng

Thêm, sửa, xoá sản phẩm; upload ảnh (kiểm tra đúng là file ảnh); sửa bảng thông số. Sửa danh mục và thứ tự hiển thị trên trang chủ. Xem khách hàng kèm số đơn và tổng chi tiêu.

| Sản phẩm | Sửa sản phẩm |
|---|---|
| ![Sản phẩm](docs/screenshots/admin-06-products.jpg) | ![Sửa sản phẩm](docs/screenshots/admin-07-product-edit.jpg) |

| Danh mục | Khách hàng |
|---|---|
| ![Danh mục](docs/screenshots/admin-08-categories.jpg) | ![Khách hàng](docs/screenshots/admin-09-customers.jpg) |

| Đăng nhập quản trị | Mobile | Menu mobile |
|---|---|---|
| ![Đăng nhập admin](docs/screenshots/admin-01-login.jpg) | ![Admin mobile](docs/screenshots/admin-10-mobile-dashboard.jpg) | ![Menu mobile](docs/screenshots/admin-11-mobile-menu.jpg) |

---

## Chạy dự án

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # chỉnh DATABASE_PATH, SITE_NAME, hotline, BANK_INFO...
flask init-db             # tạo bảng (chạy lại sau khi cập nhật code: thêm cột mới, không mất dữ liệu)
flask seed                # nạp dữ liệu mẫu từ app/seed_data.json (DB trống)
flask create-admin        # tạo tài khoản quản trị (hỏi số điện thoại + mật khẩu)
flask run                 # cửa hàng: http://127.0.0.1:8000 — quản trị: /admin
pytest                    # chạy test
```

Muốn tạo lại DB từ đầu: xoá `instance/app.db` rồi chạy lại `init-db` và `seed`.
Dữ liệu mẫu và ảnh được sinh bởi `python3 scripts/build_seed.py` (cần mạng, đã chạy sẵn).
Muốn cấp quyền quản trị cho một tài khoản đã đăng ký, chạy `flask create-admin --phone <số> --password ""` rồi xác nhận.

## Các trang

| URL | Trang |
|---|---|
| `/` | Trang chủ |
| `/danh-muc/<slug>?hang=&gia=&sap_xep=&con_hang=1` | Danh mục và bộ lọc |
| `/tim-kiem?q=` | Tìm kiếm |
| `/san-pham/<slug>` | Chi tiết sản phẩm |
| `/dang-ky`, `/dang-nhap`, `/dang-xuat` (POST) | Tài khoản (số điện thoại + mật khẩu) |
| `/gio-hang` | Giỏ hàng (lưu trong session, khách chưa đăng nhập vẫn dùng được) |
| `/thanh-toan` | Đặt hàng: cần đăng nhập; COD hoặc chuyển khoản |
| `/don-hang`, `/don-hang/<id>` | Đơn hàng của tôi |
| `/admin` | Quản trị: tổng quan, đơn hàng, sản phẩm, danh mục, khách hàng, xuất CSV |
| `/api/products` | JSON API (GET danh sách, GET /<id>, POST) |

## Bảo mật

- **Mật khẩu:** băm bằng `werkzeug.security`.
- **Form POST:** mọi form đều có CSRF token.
- **Đăng nhập:** tạo phiên mới mỗi lần đăng nhập.
- **Chuyển hướng:** tham số `next` chỉ nhận đường dẫn nội bộ.
- **Giá và tồn kho:** luôn đọc lại từ DB lúc đặt hàng, không tin số liệu từ trình duyệt. Trừ kho bằng `UPDATE ... WHERE stock >= qty`, nên hai người đặt cùng lúc không thể làm kho bị âm.
- **Quyền quản trị:** mọi trang `/admin` đều kiểm tra quyền admin.
- **Ảnh upload:** kiểm tra nội dung file, không chỉ dựa vào đuôi file.
- **Xuất CSV:** chặn ô chạy thành công thức khi mở bằng Excel.

## Cấu trúc

```
app/
├── __init__.py              # create_app(), filter vnd, helper url_with()
├── config.py                # đọc cấu hình từ .env
├── db.py                    # kết nối SQLite + lệnh init-db, seed, create-admin
├── security.py              # CSRF, login_required, admin_required
├── schema.sql               # categories, brands, products, banners, quick_links, users, orders, order_items
├── seed_data.json           # dữ liệu mẫu
├── routes/                  # main, catalog, auth, shop, admin, products (API)
├── services/                # nghiệp vụ: product, catalog, auth, cart, order, admin
├── repositories/            # SQL thuần: product, category, content, user, order, stats
├── templates/
│   ├── base.html, pages/    # trang cửa hàng
│   ├── components/          # header, footer, menu danh mục, card, carousel... (home/, category/, product/)
│   └── admin/               # layout, macro UI và các trang quản trị
└── static/
    ├── css/                 # base.css + components/ + pages/ (cửa hàng)
    ├── js/main.js           # hành vi cửa hàng
    ├── admin/               # admin.css + admin.js
    └── img/                 # ảnh sản phẩm, banner, logo, icon
docs/research/               # khảo sát giao diện gốc (cửa hàng + admin/)
docs/screenshots/            # ảnh chụp trong README
scripts/build_seed.py        # sinh seed_data.json + tải ảnh
tests/                       # test cửa hàng, mua hàng, quản trị
```

## Nguyên tắc

1. **Không hardcode:** cấu hình, đường dẫn DB và thông tin cửa hàng lấy từ `.env`; nội dung trang (banner, danh mục, link nhanh) nằm trong DB.
2. **Phân tầng một chiều:** `routes → services → repositories → db`. Route không viết SQL, repository không chứa nghiệp vụ.
3. **SQL luôn dùng tham số `?`;** tên cột trong ORDER BY chỉ lấy từ whitelist.
4. **UI chia component:** mỗi khối giao diện là một file template và một file CSS riêng.

## Lưu ý bản quyền

Ảnh sản phẩm và banner tải từ cellphones.com.vn chỉ dùng để học và chạy local.
Không triển khai công khai với các ảnh này; hãy thay bằng ảnh của bạn trước khi deploy.
