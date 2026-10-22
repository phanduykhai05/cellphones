"""Dựng app/seed_data.json + tải ảnh về app/static/img từ dữ liệu khảo sát trong docs/research.

Chạy một lần (cần mạng):  python3 scripts/build_seed.py
Sau đó:                   flask init-db && flask seed
"""
import html
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RESEARCH = ROOT / "docs" / "research"
STATIC = ROOT / "app" / "static"
OUT = ROOT / "app" / "seed_data.json"

downloads: dict[str, str] = {}  # url -> đường dẫn tương đối trong static/


def local(url: str | None, rel_stem: str) -> str | None:
    """Đăng ký 1 ảnh cần tải, trả về đường dẫn tương đối trong static/."""
    if not url or not url.startswith("http"):
        return None
    if url in downloads:
        return downloads[url]
    ext = re.search(r"\.(png|jpe?g|webp|gif|svg)(?:$|\?)", url.split("/plain/")[-1], re.I)
    rel = f"img/{rel_stem}.{ext.group(1).lower() if ext else 'jpg'}"
    downloads[url] = rel
    return rel


def fetch(item: tuple[str, str]) -> str | None:
    url, rel = item
    dest = STATIC / rel
    if dest.exists() and dest.stat().st_size > 0:
        return None
    dest.parent.mkdir(parents=True, exist_ok=True)
    # curl dùng kho chứng chỉ của hệ điều hành (urllib của Python.org build hay thiếu CA)
    r = subprocess.run(["curl", "-sSfL", "--max-time", "30", "-A", "Mozilla/5.0", "-o", str(dest), url],
                       capture_output=True, text=True)
    if r.returncode != 0:  # ghi lại lỗi, không dừng cả mẻ
        dest.unlink(missing_ok=True)
        return f"{url} -> {r.stderr.strip()}"
    return None


def slug_of(href: str) -> str:
    return href.rstrip("/").split("/")[-1].removesuffix(".html")


def num(text: str) -> int | None:
    digits = re.sub(r"\D", "", text or "")
    return int(digits) if digits else None


BRANDS = [  # (từ khoá trong tên, tên hãng) — thứ tự quan trọng
    ("iphone", "Apple"), ("macbook", "Apple"), ("ipad", "Apple"), ("apple", "Apple"),
    ("samsung", "Samsung"), ("oppo", "OPPO"), ("poco", "Xiaomi"), ("redmi", "Xiaomi"), ("xiaomi", "Xiaomi"),
    ("honor", "HONOR"), ("asus", "ASUS"), ("msi", "MSI"), ("dell", "Dell"), ("hp ", "HP"), ("lenovo", "Lenovo"),
    ("acer", "Acer"), ("huawei", "Huawei"), ("garmin", "Garmin"), ("amazfit", "Amazfit"), ("lg ", "LG"),
    ("tcl", "TCL"), ("coocaa", "Coocaa"), ("myalo", "myALO"), ("masstel", "Masstel"), ("sony", "Sony"),
    ("toshiba", "Toshiba"), ("panasonic", "Panasonic"), ("aqua", "AQUA"), ("hitachi", "Hitachi"), ("sharp", "Sharp"),
]


def brand_of(name: str) -> str:
    low = name.lower() + " "
    return next((b for key, b in BRANDS if key in low), name.split()[0])


def category_of(name: str) -> str:
    low = name.lower()
    if re.search(r"đồng hồ|watch|vòng đeo", low):
        return "dong-ho"
    if re.search(r"tivi|tủ lạnh", low):  # sidebar gốc gộp "Tivi, Điện máy"
        return "tivi"
    if re.search(r"màn hình|display", low):
        return "man-hinh"
    if re.search(r"laptop|macbook", low):
        return "laptop"
    return "dien-thoai"


CATEGORIES = [  # slug, tên sidebar, tên tab ngắn, icon, nhóm block trang chủ (0 = không có block)
    ("dien-thoai", "Điện thoại, Tablet", "Điện thoại", "mobile", 1),
    ("laptop", "Laptop", "Laptop", "laptop", 2),
    ("am-thanh", "Âm thanh, Mic thu âm", "Âm thanh", "audio-2", 0),
    ("dong-ho", "Đồng hồ, Camera", "Đồng hồ", "watch", 3),
    ("gia-dung", "Đồ gia dụng, Làm đẹp", "Gia dụng", "home-appliances", 0),
    ("phu-kien", "Phụ kiện", "Phụ kiện", "accessories", 0),
    ("man-hinh", "PC, Màn hình, Máy in", "Màn hình máy tính", "pc", 2),
    ("tivi", "Tivi, Điện máy", "Tivi", "tv", 4),
    ("thu-cu", "Thu cũ đổi mới", "Thu cũ", "trade-in", 0),
    ("hang-cu", "Hàng cũ", "Hàng cũ", "used-goods", 0),
    ("khuyen-mai", "Khuyến mãi", "Khuyến mãi", "promotions", 0),
    ("tin-cong-nghe", "Tin công nghệ", "Tin công nghệ", "tech-news", 0),
]
CATEGORY_BANNER_ALT = {  # alt của banner trái trên trang chủ -> danh mục
    "iPhone Duo": "dien-thoai", "Banner laptop home desktop 1": "laptop",
    "Đồng hồ thông minh desktop": "dong-ho", "Banner tivi home desktop": "tivi",
}
SUB_LINKS = {  # nhãn chip danh mục con -> danh mục
    "dien-thoai": ["Điện thoại chơi game", "Điện thoại pin trâu", "Điện thoại 5G", "Điện thoại chụp ảnh đẹp",
                   "Điện thoại gập", "Điện thoại AI", "Điện thoại phổ thông"],
    "laptop": ["Văn phòng", "Gaming", "Mỏng nhẹ", "Đồ họa - kỹ thuật", "Sinh viên", "Cảm ứng", "Laptop AI"],
    "dong-ho": ["Tập luyện thể thao", "Nghe gọi", "Vòng đeo tay thông minh", "Định vị trẻ em", "Đo huyết áp", "Chống nước"],
    "tivi": ["32 inch", "43 inch", "55 inch", "60 inch", "65 inch", "75 inch", "Tivi cũ", "Giá treo tivi"],
}
ACCESSORIES = ["Phụ kiện Apple", "Cáp, sạc", "Pin sạc dự phòng", "Ốp lưng - Bao da", "Dán màn hình", "Thẻ nhớ, USB",
               "Gaming Gear, Playstation", "Sim 4G - 5G", "Thiết bị mạng", "Camera", "Gimbal", "Flycam", "Máy ảnh",
               "Chuột, bàn phím", "Balo, túi xách", "Hub chuyển đổi", "Phụ kiện điện thoại", "Phụ kiện Laptop"]


def clean_details(raw: dict, slug: str) -> dict:
    versions = [v for v in raw.get("versions", [])
                if re.fullmatch(r"\d+\s?(GB|TB)|[\w\s]{2,18}", v) and not re.search(r"đ|tháng|Kiểm tra|Xem|tùy chỉnh", v)]
    colors, seen = [], set()
    for c in raw.get("colors", []):
        if "flash_sale" in c["img"] or not c["label"]:
            continue
        m = re.match(r"(.+?)\s+([\d.]+)₫?$", c["label"])
        name = m.group(1) if m else c["label"]
        if name in seen:
            continue
        seen.add(name)
        colors.append({"name": name, "price": num(m.group(2)) if m else None,
                       "image": local(c["img"], f"products/{slug}-c{len(colors)}")})
    gallery = [local(u, f"products/{slug}-g{i}") for i, u in enumerate(raw.get("gallery", []))]
    return {
        "gallery": [g for g in gallery if g],
        "specs": raw.get("specs", []),
        "versions": versions[:6],
        "colors": colors[:6],
        "promotions": [p for p in raw.get("promos", []) if len(p) < 300][:4],
        "faqs": [q for q in raw.get("faq", []) if not re.match(r"^\d+\.", q)][:5],
    }


def main() -> None:
    home = json.loads((RESEARCH / "assets-home.json").read_text())
    plp = json.loads((RESEARCH / "extract-plp.json").read_text())
    pdp = json.loads((RESEARCH / "pdp-data.json").read_text())

    products, seen = [], set()
    for p in home["products"] + plp["products"]:
        slug = slug_of(p["href"])
        if slug in seen or not p.get("price"):
            continue
        seen.add(slug)
        old = p.get("old")
        details = clean_details(pdp.get(f"/{slug}.html", {}), slug)
        products.append({
            "slug": slug, "name": p["name"], "brand": brand_of(p["name"]), "category": category_of(p["name"]),
            "price": p["price"], "old_price": old if old and old > p["price"] else None,
            "stock": 10, "rating": float(p["rating"]) if re.fullmatch(r"\d(\.\d)?", p.get("rating") or "") else None,
            "promo": p.get("promo") or None, "image": local(p["img"], f"products/{slug}"), "details": details,
        })

    small = {i["alt"] or i["label"]: i["src"] for i in home["smallImgs"]}
    icons = {re.search(r"icon-homepage-([\w-]+)\.svg", i["src"]).group(1): i["src"]
             for i in home["smallImgs"] if "icon-homepage-" in i["src"]}
    banners_by_alt = {b["alt"]: b["src"] for b in home["banners"]}
    cat_banner = {cat: banners_by_alt.get(alt) for alt, cat in CATEGORY_BANNER_ALT.items()}

    categories = [{"slug": s, "name": n, "short_name": sn, "sort": i, "home_group": g,
                   "icon": local(icons.get(ic), f"icons/{ic}"),
                   "banner": local(cat_banner.get(s), f"banners/cat-{s}")}
                  for i, (s, n, sn, ic, g) in enumerate(CATEGORIES)]

    quick_links = []
    for cat, labels in SUB_LINKS.items():
        for i, label in enumerate(labels):
            quick_links.append({"grp": f"sub:{cat}", "label": label, "sort": i, "link": f"/danh-muc/{cat}",
                                "image": local(small.get(label), f"links/{cat}-{i}")})
    acc_imgs = [i["src"] for i in home["smallImgs"] if "page_configs" in i["src"]]
    for i, label in enumerate(ACCESSORIES):
        quick_links.append({"grp": "accessory", "label": label, "sort": i, "link": "/danh-muc/phu-kien",
                            "image": local(small.get(label) or (acc_imgs[i] if i < len(acc_imgs) else None), f"links/acc-{i}")})

    def banner_rows(position, items):
        return [{"position": position, "title": html.unescape(t), "subtitle": st, "link": "/", "sort": i,
                 "image": local(src, f"banners/{position}-{i}")} for i, (t, st, src) in enumerate(items) if src]

    by_y = sorted(home["banners"], key=lambda b: b["y"])
    hero = [b for b in by_y if b["w"] == 736]
    hero = hero[-2:] + hero[:-2]  # thứ tự tab: MỪNG KHAI TRƯƠNG, IPHONE 18 PRO, ...
    banners = []
    banners += banner_rows("hero", [(b["alt"].split("  ")[0].strip(), b["alt"].split("  ")[-1].strip(), b["src"]) for b in hero])
    banners += banner_rows("hero_small", [(b["alt"], "", b["src"]) for b in by_y if b["w"] == 240])
    banners += banner_rows("wide", [(b["alt"], "", b["src"]) for b in by_y if b["w"] == 1200 and b["h"] < 100])
    banners += banner_rows("deal_tab", [(b["alt"], "", b["src"]) for b in by_y if b["h"] in (45, 50)])
    promo = [(b["alt"], "", b["src"]) for b in home["banners"] if b["w"] == 274]  # thứ tự DOM: 4 giáo dục rồi 4 thanh toán
    banners += banner_rows("promo_edu", promo[:4])
    banners += banner_rows("promo_pay", promo[4:8])
    plp = json.loads((RESEARCH / "plp-banners.json").read_text())
    banners += banner_rows("plp", [(b["alt"], "", b["src"]) for b in plp])
    banners += banner_rows("brand_page", [(b["alt"], "", b["src"]) for b in by_y if b["w"] == 291])

    brand_logos = {}
    for i in home["smallImgs"]:
        m = re.search(r"/Brand/([\w-]+?)(?:-new)?(?:-240x50)?\.png", i["src"])
        if m:
            name = {"iPhone": "Apple", "Mastel": "Masstel", "Oppo": "OPPO", "XIAOMI": "Xiaomi", "honor": "HONOR",
                    "SONY": "Sony", "HUAWEI": "Huawei", "lenovo": "Lenovo", "tecno": "TECNO", "MEIZU": "Meizu"}.get(m.group(1), m.group(1))
            brand_logos.setdefault(name, local(i["src"], f"brands/{name.lower()}"))
    brands = [{"name": n, "logo": logo} for n, logo in brand_logos.items()]

    print(f"Tải {len(downloads)} ảnh...", flush=True)
    with ThreadPoolExecutor(8) as pool:
        errors = [e for e in pool.map(fetch, downloads.items()) if e]
    for e in errors:
        print("  lỗi:", e, file=sys.stderr)
    failed = {downloads[e.split(" -> ")[0]] for e in errors}

    def ok(rel):  # ảnh tải lỗi -> None để template dùng ảnh thay thế
        return None if rel in failed else rel

    for p in products:
        p["image"] = ok(p["image"])
        d = p["details"]
        d["gallery"] = [g for g in d["gallery"] if ok(g)]
        for c in d["colors"]:
            c["image"] = ok(c["image"])
    for row in categories + quick_links + banners:
        for k in ("icon", "banner", "image"):
            if k in row:
                row[k] = ok(row[k])
    for b in brands:
        b["logo"] = ok(b["logo"])

    OUT.write_text(json.dumps({"categories": categories, "brands": brands, "products": products,
                               "banners": [b for b in banners if b["image"]], "quick_links": quick_links},
                              ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK: {len(products)} sản phẩm, {len(banners)} banner, {len(brands)} hãng, "
          f"{len(downloads) - len(errors)}/{len(downloads)} ảnh -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
