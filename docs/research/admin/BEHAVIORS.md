# Behaviors — manifest-commerce.reui.io (admin, đo 2026-10-22 @1440)

| Thành phần | Trigger | Thay đổi | Cách làm trong bản clone |
|---|---|---|---|
| Nút panel-left trên topbar | click | thu/mở sidebar | JS toggle class `is-collapsed` trên `.adm`, nhớ trạng thái bằng localStorage |
| Nav item sidebar | hover / trang hiện tại | bg `oklab(.205 0 0 / .05)`, weight 500 | CSS + class `is-active` theo endpoint |
| Tab bảng tồn kho (All / In stock / Low / Out) | click | tab active chữ foreground (khác: foreground/60), gạch dưới `::after` cao 2px màu foreground, bottom -5px | link `?ton=...` render phía server |
| Header cột bảng | click | sort ↑↓ (icon chevrons-up-down → arrow-up/down) | link `?sap_xep=cot&chieu=asc/desc` |
| Hàng bảng | hover | bg `muted/40` | CSS |
| Nút "…" cuối hàng | click | dropdown hành động | `<details>` |
| Rows per page | change | đổi số dòng / trang | `<select>` tự submit |
| Phân trang | click | trang 1..n, active bg muted | link `?trang=` |
| Filter "contains" | gõ + Enter | lọc theo text | form GET |
| Select trạng thái / danh mục (form) | change | — | `<select>` native, style như shadcn select |
| Biểu đồ cột | load | animation cột mọc lên (recharts) | CSS `@keyframes` scaleY 0→1 .6s ease-out |
