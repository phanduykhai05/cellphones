from flask import Blueprint, render_template

from app.repositories import content_repo
from app.services import catalog_service

bp = Blueprint("main", __name__)


@bp.get("/")
def home():
    banners = {pos: content_repo.banners(pos)
               for pos in ("hero", "hero_small", "wide", "promo_edu", "promo_pay", "brand_page")}
    return render_template(
        "pages/home.html",
        banners=banners,
        deal_tabs=catalog_service.deal_tabs(),
        blocks=catalog_service.home_blocks(),
        accessories=content_repo.quick_links("accessory"),
    )
