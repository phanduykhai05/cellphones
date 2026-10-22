"""Nội dung trang: banner, link nhanh, logo hãng."""
from app.db import get_db


def banners(position: str) -> list[dict]:
    rows = get_db().execute("SELECT * FROM banners WHERE position = ? ORDER BY sort", (position,)).fetchall()
    return [dict(r) for r in rows]


def quick_links(grp: str) -> list[dict]:
    rows = get_db().execute("SELECT * FROM quick_links WHERE grp = ? ORDER BY sort", (grp,)).fetchall()
    return [dict(r) for r in rows]


def brand_logos() -> dict[str, str | None]:
    return dict(get_db().execute("SELECT name, logo FROM brands").fetchall())
