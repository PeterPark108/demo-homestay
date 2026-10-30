# Nhà Gió – bản demo web khách sạn (hotel-v2)

Website tĩnh, khách sạn **giả lập**: giá, đánh giá, địa chỉ đều là minh họa. Ảnh là ảnh thật có giấy phép Unsplash (xem `nguon-anh.html` và `assets/photos/CREDITS.md`), không chụp tại cơ sở thật. Không có dữ liệu nào gửi lên máy chủ; đặt phòng chỉ lưu trong trình duyệt.

## Mở trên máy tính
- Cách nhanh: mở thẳng file `index.html` bằng Chrome/Edge/Safari (bấm đúp).
- Cách giống web thật (khuyên dùng): trong thư mục web chạy
  ```
  python3 -m http.server 8000
  ```
  rồi mở http://localhost:8000/ . Đặt thư mục vào thư mục con nào cũng chạy (mọi liên kết đều là đường dẫn tương đối), ví dụ http://localhost:8000/nha-gio/ .

## Đường bấm thử (khoảng 1 phút)
1. **Trang chủ** (`index.html`): xem ảnh lớn, khung chọn ngày.
2. **Loại phòng**: bấm menu "Loại phòng" → lọc theo loại, số khách, sắp xếp giá.
3. **Chi tiết phòng**: bấm một phòng (ví dụ "Villa Hồ Bơi Eo Gió") → bấm ảnh để xem lớn (← → để chuyển, Esc để đóng) → chọn ngày nhận rồi ngày trả trên lịch, xem tạm tính.
4. **Đặt phòng**: bấm "Tiếp tục đặt phòng" → điền họ tên, số điện thoại, tick đồng ý.
5. **Xác nhận**: bấm "Gửi yêu cầu đặt phòng (demo)" → hiện mã tham chiếu (chỉ lưu trên trình duyệt).

## Trên điện thoại
- Mở trang (cùng mạng Wi‑Fi: `http://<IP-máy-tính>:8000/`), bấm nút **☰ Menu** góc phải để mở menu, chọn trang.
- Ảnh chụp luồng mobile 390 px: `screenshots/hotel-v2/flow-01-home.png` … `flow-06-menu.png`.

Bản cũ vẫn giữ ở `homestay-v1/index.html`.

## Chuyển động & intro
- Lần đầu mở trang chủ trong một phiên sẽ có màn intro "gió" ~2,5 giây; bấm **Bỏ qua**, Esc hoặc chạm bất kỳ đâu để vào ngay.
- Muốn xem lại intro: mở tab mới/cửa sổ ẩn danh, hoặc xóa `nhagio_intro_seen` trong sessionStorage rồi tải lại.
- Nếu máy bật "Giảm chuyển động" (Reduce motion) thì không có intro và hiệu ứng.
- Video demo mobile: `screenshots/hotel-v2/motion-demo.mp4`.
