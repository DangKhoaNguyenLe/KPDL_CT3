Tên Ứng dụng: **Tour & Travel Booking Platform**

Hệ thống bao gồm 3 thành phần chính:

## Backend (Core System)

- **Lập trình:** Python (FastAPI),
- **Cơ sở dữ liệu:** MonggoDb
- **Thư viện thuật toán:** `thuatttoan` (Chứa thuật toán tối ưu/gợi ý)

### Yêu cầu Backend:
1. **Thiết kế Schema dữ liệu:**
   - **Users:** Quản lý tài khoản khách hàng (Auth)
   - **Tours:** Thông tin chi tiết về các tour (Lịch trình, Giá, Sức chứa)
   - **Services:** Các dịch vụ đi kèm (Khách sạn, Vé máy bay, Thuê xe)
   - **Bookings:** Quản lý đơn đặt tour (Trạng thái, Ngày đi)
   - **Reviews:** Đánh giá và xếp hạng từ khách hàng.
2. **Triển khai API:**
   - Xây dựng các endpoint RESTful để phục vụ cho Frontend (GET, POST, PUT, DELETE).
   - Tích hợp thư viện `thuatttoan` để xử lý các nghiệp vụ logic (Ví dụ: Tìm kiếm tour theo tiêu chí phức tạp, Gợi ý dịch vụ bổ sung).
3. **Kết nối với frontend hiện có**
    - frontend được xây dựng trong app.py, templates
