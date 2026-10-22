# Behaviors — cellphones.com.vn (đo ngày 2026-10-22, 1440px)

| # | Thành phần | Trigger | Trạng thái A → B | Transition | Cách làm |
|---|---|---|---|---|---|
| 1 | Dải khuyến mãi trên header | scrollY > ~50px | height 18px→0, margin-top 8px→0, opacity 1→0. Header 98px→72px | `all .2s cubic-bezier(.4,0,.2,1)` | JS thêm class `is-scrolled` vào `<header>` |
| 2 | Chữ chạy trong dải khuyến mãi | time | `@keyframes scroll-left {0%{translate:0} 100%{translate:calc(-50% - 12px)}}`, nội dung nhân đôi, gap 24px | `20s linear infinite` | CSS thuần |
| 3 | Slider banner chính | time + click tab | Tự chuyển ~4.5s. Tab active: bg `#F2F2F3`, chữ đậm đỏ | đổi slide ngay | JS setInterval + click |
| 4 | Mũi tên slider | hover vùng slider | nút tròn trắng mờ 2 bên | — | CSS |
| 5 | Mega menu sidebar | hover item danh mục | panel 968×497 trắng bo 12px hiện chồng lên slider | không animation | CSS `:hover` / `:focus-within` |
| 6 | Card sản phẩm | hover | ảnh `transform` (scale) `.5s cubic-bezier(.4,0,.2,1)`; box-shadow KHÔNG đổi | .5s | CSS |
| 7 | Tab danh mục (ĐIỆN THOẠI / MÁY TÍNH BẢNG) | click | active: chữ `#D70018`, border-bottom 1px `#D70018`, nền gradient đỏ mờ từ dưới lên; inactive: chữ `#1D1D20`, border-bottom `#F2F2F3` | `all .15s` | JS đổi panel |
| 8 | Tab "Deal sốc / Hot trend / Hàng mới về" | click | tab active bo trên 16px, viền 3px `#609AFA` | — | JS |
| 9 | Carousel sản phẩm | click mũi tên | swiper ngang, 2 hàng × 4 cột (desktop) | — | `scroll-snap` + JS scrollBy |
| 10 | Link footer, link phụ kiện | hover | underline | — | CSS |
| 11 | Nút nổi "Lên đầu" / "Liên hệ" | luôn hiện (Lên đầu chỉ khi đã cuộn) | — | — | fixed bottom-right |
| 12 | Hàng chip bộ lọc (trang danh mục) | scroll | dính ngay dưới header (sticky top 72px) | — | `position: sticky` |
| 13 | Thanh mua cố định (trang chi tiết) | luôn hiện | fixed bottom, 880×80, bo 12px, shadow | — | CSS |
| 14 | Chọn phiên bản / màu (trang chi tiết) | click | viền 2px `#D70018` + dấu tick góc phải trên | — | JS / radio |
| 15 | FAQ (trang chi tiết) | click | mở/đóng câu trả lời | — | `<details>` |

Không có thư viện smooth scroll (Lenis/Locomotive). Không có animation khi phần tử vào viewport, chỉ có `animate-fade-in` khi card được tải.

## Responsive
- **≥1200px:** khung 1200px; hàng hero gồm sidebar 224 | slider 736 | cột phải 224; card 4 cột (trong block danh mục) hoặc 5 cột (trang danh mục).
- **768–1199px:** ẩn cột phải; sidebar còn ở ≥1024px.
- **<768px:** header gọn (logo dạng icon, ô tìm kiếm, nút giỏ hàng), ẩn sidebar; slider rộng toàn màn hình; card 2 cột; trang chi tiết chỉ một cột, thanh mua cố định rộng full.
