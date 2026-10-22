# Page Topology

## Trang chủ `/`
| # | Section | Loại | Tương tác | Component |
|---|---|---|---|---|
| 0 | Header (dải khuyến mãi + thanh chính) | fixed, z 1000 | scroll + time | `site_header.html` |
| 1 | Hero: sidebar danh mục, slider, cột phải | flow | hover / time / click | `home/hero.html` (`category_menu`, `mega_menu`, `hero_slider`, `hero_right`) |
| 2 | 3 banner nhỏ dưới slider | flow | static | trong `home/hero.html` |
| 3 | Banner ngang 1200×82 | flow | static | `home/wide_banner.html` |
| 4 | Khối tab Deal sốc / Hot trend / Hàng mới về | flow | click | `home/deal_tabs.html` |
| 5 | Block danh mục × N (banner trái + tab + chip + carousel 2 hàng) | flow | click | `home/category_block.html` |
| 6 | Sắm thêm phụ kiện (lưới 6×3) | flow | hover | `home/accessory_grid.html` |
| 7 | Ưu đãi giáo dục / thanh toán (2 cột × 4 banner) | flow | static | `home/promo_grid.html` |
| 8 | Chuyên trang thương hiệu (4 banner) | flow | static | `home/brand_pages.html` |
| 9 | Footer | flow | hover | `site_footer.html` |
| 10 | Nút nổi Lên đầu / Liên hệ | fixed | click | `floating_actions.html` |

## Trang danh mục `/danh-muc/<slug>`
Breadcrumb → 2 banner → H1 → lưới logo hãng → "Chọn theo nhu cầu" → hàng chip bộ lọc (sticky) → sắp xếp → lưới sản phẩm 5 cột.

## Trang chi tiết `/san-pham/<slug>`
Breadcrumb → [cột trái 592: tiêu đề, đánh giá, link hành động, gallery + thumbnail, cam kết, thông số, FAQ] | [cột phải 592: hộp giá, phiên bản, màu sắc, khuyến mãi, nút mua] → Sản phẩm tương tự → thanh mua cố định.
