CREATE TABLE IF NOT EXISTS categories (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    slug        TEXT    NOT NULL UNIQUE,
    name        TEXT    NOT NULL,
    short_name  TEXT    NOT NULL,
    icon        TEXT,
    banner      TEXT,
    home_group  INTEGER NOT NULL DEFAULT 0,  -- các danh mục cùng nhóm > 0 thành 1 block tab trên trang chủ
    sort        INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS brands (
    name  TEXT PRIMARY KEY,
    logo  TEXT
);

CREATE TABLE IF NOT EXISTS products (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    slug         TEXT    NOT NULL UNIQUE,
    name         TEXT    NOT NULL,
    brand        TEXT    NOT NULL,
    category_id  INTEGER NOT NULL REFERENCES categories(id),
    price        INTEGER NOT NULL CHECK (price >= 0),
    old_price    INTEGER CHECK (old_price IS NULL OR old_price >= price),
    stock        INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    rating       REAL,
    promo        TEXT,
    image_url    TEXT,
    details      TEXT    NOT NULL DEFAULT '{}',  -- JSON chỉ để hiển thị: gallery, specs, versions, colors, promotions, faqs
    created_at   TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);

CREATE TABLE IF NOT EXISTS banners (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    position  TEXT    NOT NULL,  -- hero, hero_small, wide, deal_tab, promo_edu, promo_pay, brand_page
    title     TEXT    NOT NULL DEFAULT '',
    subtitle  TEXT    NOT NULL DEFAULT '',
    image     TEXT    NOT NULL,
    link      TEXT    NOT NULL DEFAULT '/',
    sort      INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS quick_links (
    id     INTEGER PRIMARY KEY AUTOINCREMENT,
    grp    TEXT    NOT NULL,  -- "sub:<slug danh mục>" hoặc "accessory"
    label  TEXT    NOT NULL,
    image  TEXT,
    link   TEXT    NOT NULL DEFAULT '/',
    sort   INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS users (
    id             INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    phone          TEXT    NOT NULL UNIQUE,
    email          TEXT,
    password_hash  TEXT    NOT NULL,
    is_admin       INTEGER NOT NULL DEFAULT 0,
    created_at     TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id         INTEGER NOT NULL REFERENCES users(id),
    name            TEXT    NOT NULL,
    phone           TEXT    NOT NULL,
    address         TEXT    NOT NULL,
    note            TEXT    NOT NULL DEFAULT '',
    payment_method  TEXT    NOT NULL CHECK (payment_method IN ('cod', 'bank')),
    status          TEXT    NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'paid', 'shipping', 'done', 'cancelled')),
    total           INTEGER NOT NULL CHECK (total >= 0),
    created_at      TEXT    NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);

CREATE TABLE IF NOT EXISTS order_items (
    order_id    INTEGER NOT NULL REFERENCES orders(id),
    product_id  INTEGER NOT NULL REFERENCES products(id),
    name        TEXT    NOT NULL,  -- chụp lại tên/giá lúc đặt, đơn cũ không đổi khi sản phẩm đổi giá
    variant     TEXT    NOT NULL DEFAULT '',
    image_url   TEXT,
    price       INTEGER NOT NULL CHECK (price >= 0),
    qty         INTEGER NOT NULL CHECK (qty > 0)
);
