# ProductCard
- Target: `components/product_card.html`, CSS `components/product-card.css`
- Interaction: hover (ảnh phóng nhẹ)

## Styles
- slot: padding 6px 4px
- card: bg #fff, radius 16px, flex column, min-height 204, shadow `0 4px 20px -8px rgba(0,0,0,.11), 0 0 10px rgba(0,0,0,.06)`, position relative
- link: flex 1, padding 10px 10px 0
- media: khung vuông, ảnh object-fit contain, transition transform .5s cubic-bezier(.4,0,.2,1); card:hover ảnh scale 1.05
- name h3: 14px/21px 700 #18181B, clamp 2 dòng, margin-bottom 4px, height 42
- price row: flex gap 6px, align center, mb 4px; giá 16px/24px 700 #C40016; giá gốc 12px #71717A gạch ngang, weight 500
- smember: 10px/15px 500, color #1E478A, bg #DBE8FE, padding 2px 4px, radius 4px, mb 4px ("Smember giảm đến X")
- promo box: 12px/18px #18181B, bg #F2F2F3, padding 4px, radius 4px, clamp 2 dòng
- badge "Giảm X%": absolute top -6px left 10px, 78×22, nền đỏ dạng ribbon (`#D70018` bo 3px + tam giác đậm hơn bên trái), chữ trắng 10px 500, "Giảm" + số 12px 700
- badge "Trả góp 0%": absolute top 0 right -5px, 75×29, chữ #3B82F6 10px ("0%" 12px 500); nền xanh nhạt bo, góc phải có nếp gấp tam giác #1E478A
- footer: padding 6px 10px 10px, flex space-between; badge giao nhanh: icon xe tải + "2 Giờ" chữ trắng 12px trên nền #3B82F6 bo phải 4px; sao vàng #FFC400 16px + điểm 12px 600; nút tim 32×32 tròn, icon 22px #3B82F6
- tag thông số (trang danh mục): 11px/16.5px #3A3A3A, padding 1px 5px, border 1px #D1D5DB, radius 5px, gap 10px
- badge "Hàng mới về": 12px #1B4C2F bg #DFF9E8 padding 4px 8px radius 4px
