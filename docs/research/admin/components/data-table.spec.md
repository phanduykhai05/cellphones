# Data table (orders / products / inventory)
- toolbar (trong frame, trên bảng): padding 8px 16px; "Filters" button outline (h 32, padding 0 10px, radius 10, border, 14px/500, gap 6); filter chip = nhóm 3 phần dính nhau [icon + Field] [contains muted] [input 175px] [x], viền chung, radius 10; "Clear" outline căn phải
- th: h 40 (orders: 32), padding 0 12px, 14px/500 foreground, border-bottom; icon chevrons-up-down 14px muted, cột đang sort: arrow-up/down
- td: padding 8px 12px (cột đầu padding-left 16px), 14px/20px, border-bottom (trừ hàng cuối); hàng cao ~59px; hover bg muted/40
- ô sản phẩm: thumb 42×42 radius 10 bg muted, object-fit cover + tên 14/500 + dòng phụ 12px muted (SKU mono • vendor)
- ô khách: avatar 32 tròn (ảnh hoặc chữ viết tắt bg muted) + tên 14/500 + email 14 muted
- số đơn: font mono 14/500; ngày 12 muted; tổng 14/600
- cuối hàng: nút "…" 28×28 radius 8 ghost
- footer: padding 8px 16px; "Rows per page" 14 muted + select (h 28, radius 8, border); phải: "1 - 8 of 49" 14 muted + nút trang 28×28 radius 8 (active bg muted, color .205; khác muted-foreground) + chevrons
- tabs (inventory): gap 20px, tab 14/500 padding 2px 0 12px, inactive foreground/60, active foreground + ::after 2px foreground bottom -5px; count pill
