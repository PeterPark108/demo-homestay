# Nhà Gió Homestay – web app DEMO (dữ liệu mẫu)

Bản demo đặt phòng homestay kiểu Airbnb cho một homestay **giả lập** ở Quy Nhơn (Bình Định).
HTML/CSS/JS thuần, không backend, không CDN, không thư viện ngoài. Chạy offline bằng cách mở `index.html` trực tiếp (file://).
**Mọi dữ liệu là mẫu; không có thanh toán thật; không gửi email/SMS; không đưa lên máy chủ nào.**

## Cách xem thử
1. Mở `index.html` bằng Chrome/Edge/Firefox (nhấp đúp là được).
2. Khách: Trang chủ → tìm theo ngày/số khách → chọn phòng → chọn ngày trên lịch → **Đặt phòng** → điền form → **Xác nhận** → nhận mã.
3. Chủ nhà: bấm **🔑 Quản lý (chủ nhà)** (vai trò demo, không mật khẩu) → đặt phòng vừa tạo hiện ngay ở mục *Chờ xác nhận*.
4. Nút **Khôi phục dữ liệu mẫu** trên banner sẽ xóa dữ liệu bạn tạo và nạp lại dữ liệu mẫu.

## Trang (hash-router)
| Đường dẫn | Nội dung |
|---|---|
| `#/` | Trang chủ: hero + ô tìm kiếm, danh mục nhanh, phòng nổi bật, vị trí (bản đồ SVG), tiện ích, đánh giá |
| `#/phong` | Danh sách: lọc giá / số khách / loại phòng / danh mục / tiện nghi / ngày trống, sắp xếp, yêu thích, trạng thái rỗng |
| `#/phong/:id` | Chi tiết: carousel + ảnh nhỏ, mô tả, tiện nghi, nội quy, đánh giá, bản đồ, khung đặt phòng có lịch tự vẽ (ngày kín bị khóa), số khách, tính giá |
| `#/dat-phong/:id?ci=&co=&g=` | Form khách (kiểm tra hợp lệ), tóm tắt giá |
| `#/thanh-cong/:ma` | Màn hình thành công + mã đặt phòng |
| `#/yeu-thich` | Phòng đã lưu yêu thích |
| `#/quan-ly` | Tổng quan: doanh thu, lấp đầy, đặt mới, khách sắp đến, biểu đồ SVG, việc cần xử lý |
| `#/quan-ly/dat-phong` | Danh sách đặt phòng, lọc 5 trạng thái, tìm kiếm, đổi trạng thái |
| `#/quan-ly/lich` | Lịch phòng theo tháng (dạng Gantt) |
| `#/quan-ly/phong` | Sửa giá, phí dọn, tình trạng (Hoạt động/Tạm ngưng), thêm phòng |

## Tính giá
`giá/đêm × số đêm + phí dọn dẹp + phí dịch vụ 5%` (làm tròn nghìn). Tối đa 30 đêm/lần đặt.

## Dữ liệu
- 7 phòng, ~25 đặt phòng, ~25 đánh giá – tạo bằng bộ sinh số ngẫu nhiên cố định, ngày tính quanh ngày hiện tại.
- Lưu localStorage: `nhagio_db_v1` (phòng, đặt phòng, đánh giá), `nhagio_fav` (yêu thích).
- Tên khách, SĐT, email (`@vidu.test`), địa chỉ, hotline đều là giả.

## Ảnh
Tất cả ảnh phòng/phong cảnh là **tranh minh họa SVG tự vẽ bằng code** (`js/art.js`), không dùng ảnh chụp, ảnh người thật hay ảnh có bản quyền. Biểu tượng tiện nghi dùng emoji hệ thống.

## Cấu trúc
`index.html`, `css/app.css`, `js/data.js` (dữ liệu & lưu trữ), `js/art.js` (ảnh SVG), `js/app.js` (router & trang khách), `js/admin.js` (trang quản lý), `screenshots/`.

## Hạn chế
- Chỉ là demo phía trình duyệt: dữ liệu nằm trong localStorage của từng trình duyệt, không đồng bộ giữa máy; không đăng nhập thật, không thanh toán, không gửi xác nhận.
- Ô chọn ngày ở trang chủ/danh sách dùng `input type=date` của trình duyệt (định dạng hiển thị theo ngôn ngữ máy); lịch tự vẽ nằm ở trang chi tiết.
- Bản đồ là hình minh họa, không theo tỉ lệ; không có bản đồ thật.
- Chưa có kéo-thả trên lịch quản lý, chưa có giá theo mùa/cuối tuần, chưa có đa ngôn ngữ.

## v2 – áp design-spec.md
- **Token** trong `:root` (`--color-*`, `--fs-*`, `--sp-*`, `--radius-*`, `--shadow-*`, `--focus-ring`, `--header-h`); alias cũ (`--acc`, `--ink`…) vẫn giữ cho giai đoạn chuyển. Lớp ghi đè v2 nằm cuối `css/app.css`.
- Nút chính `#b5472c` (hover `#9a3a22`), link/eyebrow `#b5472c`, viền ô nhập `--color-border-strong #a8917c`, focus ring cho mọi control.
- Toast có viền + shadow, tự ẩn sau 3s (tôn trọng `prefers-reduced-motion`), căn giữa trên mobile, nằm trên thanh đặt phòng khi có.
- Lịch: 7 trạng thái tách biệt (trống, hover/focus, hôm nay, đã chọn, trong khoảng, đã qua, đã kín), ô 40px, không khe – dải chọn liền; khung đặt phòng 380px (440px ở ≥1100px), 1 tháng.
- Thẻ phòng flex column, tiêu đề 1 dòng, giá thẳng đáy, hover (chỉ thiết bị có chuột) + focus bàn phím.
- Quản lý: sidebar 232px ở ≥1100px (tab ngang khi nhỏ hơn, có mờ dần báo cuộn), ô bảng 12px 16px, cột tiền căn phải, badge trạng thái có chấm, nút "Lưu" chỉ chuyển màu chính khi hàng có thay đổi; bảng mobile thành thẻ.
- Ảnh chụp mới: `screenshots/v2-*.png`.
