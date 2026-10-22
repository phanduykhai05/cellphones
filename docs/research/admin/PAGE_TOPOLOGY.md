# Admin topology

Khung chung (`admin/base.html`):
- **Topbar** sticky, cao 51px, border-bottom: nút panel-left 28×28 | logo + tên store (12.8px/500) | "/" | breadcrumb trang (14px) ...... badge trạng thái (h 28, viền border, radius 8; badge "Attention" màu warning).
- **Sidebar** rộng 259px (227 + padding 16), border-right: ô tìm kiếm (h 32, radius 10, kbd ⌘K) → nhóm "Store" (label 12px/500) → item (h 32, padding 8, radius 8, gap 8, icon 16) → nhóm "System" → (dưới cùng) card quảng cáo + user (avatar 28 radius 8 bg primary, tên 14/500, email 12 muted).
- **Main** padding 24px 24px: tiêu đề trang 20px/600 tracking -0.5px + badge đếm (pill muted 12px/500) | nhóm nút phải.

| Trang | Route | Thành phần |
|---|---|---|
| Đăng nhập | `/admin/dang-nhap` | card 418px giữa màn hình |
| Dashboard | `/admin` | 4 KPI frame → [biểu đồ cột sọc 2/3 | top danh mục 1/3] → frame bảng tồn kho có tab + phân trang |
| Đơn hàng | `/admin/don-hang` | frame: thanh lọc + bảng + phân trang |
| Chi tiết đơn | `/admin/don-hang/<id>` | 2 cột: sản phẩm + giao hàng | trạng thái (form) |
| Sản phẩm | `/admin/san-pham` | frame: thanh lọc + bảng + phân trang |
| Thêm/sửa SP | `/admin/san-pham/moi`, `/admin/san-pham/<id>` | 2 cột: General / Media / Thông số | Organization |
| Danh mục | `/admin/danh-muc` | frame bảng |
| Khách hàng | `/admin/khach-hang` | frame bảng |
