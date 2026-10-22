# HeroSlider
- Target: `components/home/hero_slider.html`, CSS `hero.css`, JS `main.js`
- Interaction: time-driven (4.5s) + click tab + click mũi tên

## Styles
- wrapper: width 736, height 372, radius 12px, overflow hidden, shadow giống sidebar
- thanh tab (trên): height 44px, nền trắng, cuộn ngang; tab: padding 8px 20px, font 12px #71717A, căn giữa, 2 dòng (khối chữ cao 28px): dòng 1 `<b>` 700 in hoa, dòng 2 thường
- tab active: bg #F2F2F3, margin 0 36px, padding 8px 2px; dòng 1 màu red-600 (#E7000B)
  - 2 "vai" SVG 36×44 absolute top 0, left/right -35px (vai trái `scaleX(-1)`), viewBox gốc 1024×1362 `preserveAspectRatio=none`,
    fill #F2F2F3 phía trong đường cong chữ S: tiếp tuyến ngang ở góc trên-ngoài → dốc ở giữa → tiếp tuyến ngang ở góc dưới-trong
    ⇒ tab active rộng ở mép trên, thắt dần xuống dưới (như tab treo từ mép trên)
- mũi tên thanh tab: 18×36 (aspect 1/2), nền trắng, bo pill phía trong, shadow `0 1px 3px rgba(0,0,0,.1)`, z 20, chỉ hiện khi hover thanh tab
- ghi chú: tab đầu ("MỪNG KHAI TRƯƠNG") trên site gốc không bọc `<b>` (lỗi nội dung CMS) — bản clone giữ đậm cho mọi tab
- slide: ảnh 736×320, object-fit cover
- mũi tên: 40×80 nửa viên thuốc, bg rgba(255,255,255,.5)→.8 khi hover, icon chevron 20px #1D1D20, ở mép trái/phải (bo phía trong)

## Nội dung (theo thứ tự)
MỪNG KHAI TRƯƠNG / Ưu đãi cực khủng · IPHONE 18 PRO / Mua ngay · GALAXY Z8 SERIES / Gập mở đẳng cấp · OPPO FIND X10 SERIES / Đăng ký nhận tin · IPHONE DUO / Đăng ký nhận tin · ASUS VIVOBOOK S / Giá ưu đãi · HONOR 600S 5G / Ưu đãi mở bán · TAI NGHE SENNHEISER / Mua ngay giá sốc!
