# Form sản phẩm (New/Edit product)
- layout: grid [1fr 320px] gap 16px; tiêu đề trang 20/600 + phụ đề 14 muted; nút phải Cancel (outline) + Save (primary) h 32 radius 10
- card "General": frame với title 14/600; panel padding 0; mỗi field là 1 hàng grid [224px 1fr] gap 12px padding 16px 24px, ngăn bằng border-bottom dashed giữa các hàng; label 16px/22px? (thực tế 14px 500) + help 14px/21px muted
- input/select: h 32, padding 8px 10px, border 1px var(--input), radius 10px, 14px; focus ring 3px ring/50 + border ring
- textarea: min-h 112, padding 8px 10px, radius 10, resize vertical
- Media: dropzone border 1px dashed muted-foreground/25, radius 10, padding 16, gap 12; nút "Add files" outline nhỏ (h 28, 12.8px) + thumbnail 48×48 radius 8
- sidebar cards: Status (select có chấm màu: active emerald, draft yellow), Organization (label 14/500 + control, gap 8, các nhóm cách 16)
