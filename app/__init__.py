from dotenv import load_dotenv

load_dotenv()  # phải chạy trước khi import config: Config đọc os.environ lúc import

from flask import Flask, request, url_for  # noqa: E402

from app import db  # noqa: E402
from app.config import Config  # noqa: E402
from app import security  # noqa: E402
from app.routes import admin, auth, catalog, main, products, shop  # noqa: E402
from app.services import cart_service, catalog_service  # noqa: E402


def vnd(n: int | None) -> str:
    """30990000 -> "30.990.000đ" (định dạng giá như site gốc)."""
    return "" if n is None else f"{n:,}".replace(",", ".") + "đ"


def url_with(**changes) -> str:
    """URL trang hiện tại, giữ query string cũ và đổi/xoá (None) vài tham số."""
    args = request.args.to_dict()
    for key, value in changes.items():
        if value is None:
            args.pop(key, None)
        else:
            args[key] = value
    return url_for(request.endpoint, **(request.view_args or {}), **args)


def create_app(overrides: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    if overrides:
        app.config.update(overrides)

    db.init_app(app)
    app.add_template_filter(vnd, "vnd")
    app.add_template_global(url_with)
    app.add_template_global(security.csrf_token)
    app.before_request(security.load_user)
    app.before_request(security.check_csrf)

    @app.context_processor
    def layout_data():
        # Header (menu danh mục + mega menu) xuất hiện ở mọi trang
        return {"site": app.config, "nav_categories": catalog_service.categories(),
                "mega_menus": catalog_service.mega_menus(), "price_ranges": catalog_service.PRICE_RANGES,
                "cart_count": cart_service.count()}

    app.register_blueprint(main.bp)
    app.register_blueprint(catalog.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(shop.bp)
    app.register_blueprint(admin.bp)
    return app
