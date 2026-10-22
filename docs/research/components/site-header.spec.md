# SiteHeader
- Target: `app/templates/components/site_header.html`, CSS `app/static/css/components/header.css`
- Screenshot: `docs/design-references/home-1440-00.png` (đầu trang), `home-1440-01.png` (đã cuộn)
- Interaction: scroll-driven (thu gọn) + time-driven (chữ chạy)

## Styles
- header: fixed top 0, z 1000, width 100%, `background-image: linear-gradient(in oklab, #E45464 0px, #D70018 100%)` (hướng mặc định là từ trên xuống), color #fff
- strip (dải khuyến mãi): max-width 1200, margin-top 8px, height 18px, padding 0 4px, font 12px/16px, gap 24px, overflow hidden, transition all .2s cubic-bezier(.4,0,.2,1)
  - track: flex gap 24px, animation scroll-left 20s linear infinite
  - item: flex gap 4px, nowrap, hover scale .95 (transition .3s); chữ đậm (`<b>`) cho cụm nhấn mạnh
  - link phải ("Cửa hàng gần bạn | Tra cứu đơn hàng | 1800 2097"): flex gap 30px, có dấu phân cách `|`
- bar: max-width 1200, height 72px, padding 16px 4px, flex, gap 12px, align center
- logo link: height 40px, width ~169
- nút "Danh mục" và "Hồ Chí Minh": bg #E45464, padding 8px 16px, height 40, radius 8px, font 14px/21px, gap 4px; icon 20px + chevron
- ô tìm kiếm: flex 1, height 40, bg #fff, border 1px #CFCFD3, radius 6px (vỏ ngoài 8px), padding 8px, gap 8px; input 16px/24px màu #52525B, placeholder "Bạn muốn mua gì hôm nay?"
- "Giỏ hàng": trong suốt, padding 8px 16px, 14px; badge số đỏ/vàng 16px
- "Đăng nhập": bg #E45464, padding 8px 16px, radius 8px

## States
- scrollY > 50: strip height 0, margin-top 0, opacity 0 → header còn 72px
- spacer dưới header: 96px (h-24)

## Responsive
- <768: ẩn strip-right, nút Danh mục, chữ trong nút; logo dạng ô vuông chữ "S"; ô tìm kiếm co lại
