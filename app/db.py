"""Kết nối SQLite: mỗi request một connection, tự đóng khi xong."""
import json
import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g

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


def init_db() -> None:
    get_db().executescript((HERE / "schema.sql").read_text(encoding="utf-8"))


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
def init_db_command() -> None:
    """Tạo bảng từ schema.sql."""
    init_db()
    click.echo("Đã khởi tạo database.")


@click.command("seed")
def seed_command() -> None:
    """Nạp dữ liệu mẫu từ seed_data.json (chạy trên DB trống)."""
    seed()
    click.echo("Đã nạp dữ liệu mẫu.")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_command)
