# Cellphone Python

Web bán điện thoại bằng Flask + SQLite. Giao diện dựng theo cấu trúc của cellphones.com.vn (tài liệu khảo sát ở `docs/research/`).

## Chạy

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # chỉnh DATABASE_PATH, SITE_NAME, hotline...
flask init-db             # tạo bảng từ app/schema.sql
flask seed                # nạp dữ liệu mẫu từ app/seed_data.json (DB trống)
flask run                 # http://127.0.0.1:8000
pytest                    # chạy test
```

Muốn tạo lại DB từ đầu: xoá `instance/app.db` rồi chạy lại `init-db` + `seed`.
Dữ liệu mẫu + ảnh được sinh bởi `python3 scripts/build_seed.py` (cần mạng, đã chạy sẵn).

## Trang

| URL | Trang |
|---|---|
| `/` | Trang chủ |
| `/danh-muc/<slug>?hang=&gia=&sap_xep=&con_hang=1` | Danh mục + bộ lọc |
| `/tim-kiem?q=` | Tìm kiếm |
| `/san-pham/<slug>` | Chi tiết sản phẩm |
| `/dang-ky`, `/dang-nhap`, `/dang-xuat` (POST) | Tài khoản (số điện thoại + mật khẩu) |
| `/gio-hang` | Giỏ hàng (lưu trong session, khách chưa đăng nhập vẫn dùng được) |
| `/thanh-toan` | Đặt hàng — cần đăng nhập; COD hoặc chuyển khoản (`BANK_INFO` trong `.env`) |
| `/don-hang`, `/don-hang/<id>` | Đơn hàng của tôi |
| `/api/products` | JSON API (GET list, GET /<id>, POST) |
| `/admin` | Trang quản trị (giao diện theo template Manifest Commerce): tổng quan, đơn hàng, sản phẩm, danh mục, khách hàng, xuất CSV |

Tạo tài khoản quản trị (hoặc cấp quyền cho số điện thoại đã đăng ký):

```bash
flask init-db          # chạy lại sau khi cập nhật code: thêm cột mới, không mất dữ liệu
flask create-admin     # hỏi số điện thoại + mật khẩu
```

Bảo mật: mật khẩu băm bằng `werkzeug.security`; mọi form POST có CSRF token; phiên mới khi đăng nhập;
`next` chỉ nhận đường dẫn nội bộ; giá và tồn kho luôn đọc lại từ DB lúc đặt (trừ kho bằng `UPDATE ... WHERE stock >= qty`).

## Cấu trúc

```
app/
├── __init__.py              # create_app(), filter vnd, helper url_with()
├── config.py                # đọc cấu hình từ .env (DB, tên cửa hàng, hotline)
├── db.py                    # kết nối SQLite + lệnh `flask init-db`, `flask seed`
├── schema.sql               # categories, brands, products, banners, quick_links
├── seed_data.json           # dữ liệu mẫu
├── routes/                  # main (trang chủ), catalog (danh mục/chi tiết/tìm kiếm), products (API)
├── services/                # product_service, catalog_service: nghiệp vụ + ghép dữ liệu trang
├── repositories/            # SQL thuần: product_repo, category_repo, content_repo
├── templates/
│   ├── base.html
│   ├── pages/               # home, category, product
│   └── components/          # header, footer, menu danh mục, card, carousel, breadcrumb, icons
│       ├── home/            # hero, deal_tabs, category_block, accessory_grid, promo_grid, brand_pages
│       ├── category/        # filter_bar
│       └── product/         # gallery, price_box, options, promotions, buy_actions, specs, faq, ...
└── static/
    ├── css/base.css         # design tokens + phần dùng chung
    ├── css/components/      # 1 file / component
    ├── css/pages/           # 1 file / trang
    ├── js/main.js           # hành vi: header thu gọn, slider, tab, carousel, gallery
    └── img/                 # ảnh tải về (products, banners, brands, icons, links)
docs/research/               # khảo sát trang gốc: BEHAVIORS, PAGE_TOPOLOGY, spec từng component
scripts/build_seed.py        # sinh seed_data.json + tải ảnh
```

## Nguyên tắc

1. **Không hardcode**: cấu hình/đường dẫn DB/thông tin cửa hàng lấy từ `.env`; nội dung trang (banner, danh mục, link nhanh) nằm trong DB.
2. **Phân tầng một chiều**: `routes → services → repositories → db`. Route không viết SQL, repository không chứa nghiệp vụ.
3. **SQL luôn dùng tham số `?`**; tên cột/ORDER BY chỉ lấy từ whitelist.
4. **UI chia component**: mỗi khối giao diện 1 file template + CSS riêng; giá trị CSS đối chiếu `docs/research/components/*.spec.md`.
5. Thêm trang mới: route trong `routes/`, ghép dữ liệu ở `services/`, template trong `pages/` dùng lại `components/`.

## Lưu ý bản quyền

Ảnh sản phẩm/banner tải từ cellphones.com.vn chỉ dùng để học và chạy local. Không triển khai công khai với các ảnh này;
thay bằng ảnh của bạn trước khi deploy.
