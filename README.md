# Cellphone Python

Ứng dụng web Flask, dùng SQLite cục bộ.

## Chạy

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # chỉnh DATABASE_PATH, SECRET_KEY
flask init-db             # tạo bảng từ app/schema.sql
flask run                 # http://127.0.0.1:5000
pytest                    # chạy test
```

## Cấu trúc

```
app/
├── __init__.py          # create_app(): app factory, đăng ký blueprint
├── config.py            # đọc cấu hình từ .env
├── db.py                # kết nối SQLite + lệnh `flask init-db`
├── schema.sql           # định nghĩa bảng
├── routes/              # HTTP layer: nhận request, trả response
├── services/            # nghiệp vụ + validate
├── repositories/        # SQL thuần
├── templates/
│   ├── base.html        # layout chung
│   ├── components/      # partial tái sử dụng (header, footer, card...)
│   └── pages/           # từng trang, extends base.html
└── static/{css,js,img}
instance/                # chứa file .db (không commit)
tests/
```

## Nguyên tắc

1. **Không hardcode** cấu hình/đường dẫn DB/secret, mọi thứ lấy từ `.env` qua `config.py`.
2. **Phân tầng một chiều**: `routes → services → repositories → db`. Route không viết SQL, repository không chứa nghiệp vụ.
3. **SQL luôn dùng tham số `?`**, không nối chuỗi (chống SQL injection).
4. **UI chia components**: phần lặp lại đặt ở `templates/components/`, trang đặt ở `templates/pages/`.
5. Thêm tính năng mới: thêm bảng ở `schema.sql`, rồi tạo `repositories/x_repo.py`, `services/x_service.py`, `routes/x.py` và đăng ký blueprint trong `app/__init__.py`.
# cellphones
