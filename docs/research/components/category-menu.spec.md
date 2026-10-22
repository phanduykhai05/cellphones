# CategoryMenu + MegaMenu
- Target: `components/category_menu.html`, CSS `components/hero.css`
- Screenshot: `sidebar-megamenu-hover.png`
- Interaction: hover-driven

## Styles
- panel: width 224, height 497, bg #fff, radius 12px, padding 8px 0, shadow `0 4px 20px -8px rgba(0,0,0,.11), 0 0 10px rgba(0,0,0,.06)`, overflow-y auto
- item `<a>`: min-height 40px, padding 0 12px, flex align center; icon 24px (ảnh svg), gap 16px; text 12px/16px weight 600 #1D1D20; chevron bên phải #71717A
- item:hover: bg #F2F2F3 (neutral-100), text #D70018
- mega panel: absolute, nằm ngay bên phải sidebar (left 232), top 0, width 968, height 497, bg #fff, radius 12px, shadow như panel, padding 16px, grid 3 cột
  - tiêu đề nhóm 14px/600 #1D1D20 ("Hãng điện thoại", "Mức giá điện thoại", "Điện thoại HOT ⚡")
  - ô logo hãng: 90×40, border 1px #E4E4E7, radius 6px, padding 4px 8px, ảnh contain
  - chip giá / chip hot: 12px, padding 6px 8px, border 1px #E4E4E7, radius 6px; nhãn "Mới"/"Hot" 8px nền đỏ bo 4px ở góc trên phải
