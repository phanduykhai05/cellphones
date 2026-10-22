# CategoryBlock (trang chủ)
- Target: `components/home/category_block.html`, CSS `components/home.css`
- Interaction: click (tab + mũi tên carousel)

## Layout
- grid: banner trái 224 (ảnh 224×555, radius 12px) | nội dung 960, gap 16px
- tabs: flex, height 60; tab: flex 1, padding 0 16px, 16px/24px 600 uppercase, căn giữa
  - active: color #D70018, border-bottom 1px #D70018, `background-image: linear-gradient(to top, rgba(215,0,24,.11) 5%, rgba(255,255,255,.05) 60%)`
  - inactive: color #1D1D20, border-bottom 1px #F2F2F3
- chip danh mục con: 153×58, bg #F2F2F3, border 1px #F2F2F3, radius 8px, padding 4px 2px, gap 4px; ảnh 48×48; chữ 14px/21px 600 #1D1D20, clamp 2 dòng
- chip hãng: padding 6px 12px, border 1px #CFCFD3, radius 9999px, nền trắng, 14px/21px 500 #1D1D20, gap 8px
- "Xem tất cả": 12px 500 #3B82F6 + chevron
- carousel: 2 hàng × 4 cột (card 237 tính cả slot), mũi tên tròn 40px nền trắng, shadow, nằm sát mép phải
- khoảng cách giữa các block: my 24px
