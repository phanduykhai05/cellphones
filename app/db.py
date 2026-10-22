"""Kết nối SQLite: mỗi request một connection, tự đóng khi xong."""
import json
import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext

HERE = Path(__file__).parent


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        path = current_app.config["DATABASE_PATH"]
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        g.db = sqlite3.connect(path)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_=None) -> None:
    conn = g.pop("db", None)
    if conn is not None:
        conn.close()


# Cột thêm sau khi DB đã có dữ liệu: CREATE TABLE IF NOT EXISTS không tự thêm cột vào bảng cũ
MIGRATIONS = [("users", "is_admin", "INTEGER NOT NULL DEFAULT 0")]


def init_db() -> None:
    db = get_db()
    db.executescript((HERE / "schema.sql").read_text(encoding="utf-8"))
    for table, column, ddl in MIGRATIONS:
        if column not in {r["name"] for r in db.execute(f"PRAGMA table_info({table})")}:
            db.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")
    db.commit()


def seed(path: Path = HERE / "seed_data.json") -> None:
    """Nạp dữ liệu mẫu (sinh bởi scripts/build_seed.py) vào DB trống."""
    data = json.loads(path.read_text(encoding="utf-8"))
    db = get_db()
    db.executemany(
        "INSERT INTO categories (slug, name, short_name, icon, banner, home_group, sort)"
        " VALUES (:slug, :name, :short_name, :icon, :banner, :home_group, :sort)", data["categories"])
    db.executemany("INSERT INTO brands (name, logo) VALUES (:name, :logo)", data["brands"])
    cat_ids = dict(db.execute("SELECT slug, id FROM categories").fetchall())
    db.executemany(
        "INSERT INTO products (slug, name, brand, category_id, price, old_price, stock, rating, promo, image_url, details)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        [(p["slug"], p["name"], p["brand"], cat_ids[p["category"]], p["price"], p["old_price"], p["stock"],
          p["rating"], p["promo"], p["image"], json.dumps(p["details"], ensure_ascii=False)) for p in data["products"]])
    db.executemany(
        "INSERT INTO banners (position, title, subtitle, image, link, sort)"
        " VALUES (:position, :title, :subtitle, :image, :link, :sort)", data["banners"])
    db.executemany(
        "INSERT INTO quick_links (grp, label, image, link, sort) VALUES (:grp, :label, :image, :link, :sort)",
        data["quick_links"])
    db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command() -> None:
    """Tạo bảng từ schema.sql."""
    init_db()
    click.echo("Đã khởi tạo database.")


@click.command("seed")
@with_appcontext
def seed_command() -> None:
    """Nạp dữ liệu mẫu từ seed_data.json (chạy trên DB trống)."""
    seed()
    click.echo("Đã nạp dữ liệu mẫu.")


@click.command("create-admin")
@with_appcontext
@click.option("--phone", prompt="Số điện thoại")
@click.option("--name", default="Quản trị viên", show_default=True)
@click.password_option("--password", prompt="Mật khẩu (bỏ trống nếu chỉ cấp quyền cho tài khoản có sẵn)", default="",
                       show_default=False)
def create_admin_command(phone: str, name: str, password: str) -> None:
    """Tạo tài khoản admin, hoặc cấp quyền admin cho số điện thoại đã đăng ký."""
    from app.repositories import user_repo
    from app.services import auth_service
    user = user_repo.find_by_phone(auth_service.normalize_phone(phone))
    if user is None:
        try:
            user_id = auth_service.register(name, phone, password)
        except ValueError as e:
            raise click.ClickException(str(e))
    else:
        user_id = user["id"]
    user_repo.set_admin(user_id, True)
    click.echo(f"Đã cấp quyền admin cho {phone}.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
    app.cli.add_command(create_admin_command)
