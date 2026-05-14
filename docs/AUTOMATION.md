# Hệ thống Tự động hóa (Automation System)

Hệ thống sử dụng thư viện `APScheduler` để chạy các tác vụ nền (background jobs) tự động nhằm quản lý nghiệp vụ thư viện mà không cần sự can thiệp thủ công của nhân viên.

## 1. Cấu hình chính (backend/automation.py)

Các tham số quan trọng có thể điều chỉnh tại đầu file `automation.py`:

| Tham số | Giá trị mặc định | Mô tả |
|---------|------------------|-------|
| `FINE_PER_DAY_OVERDUE` | 10,000 VNĐ | Tiền phạt cho mỗi ngày quá hạn trả sách. |
| `LOST_BOOK_COEFFICIENT` | 2.0 | Hệ số phạt khi làm mất sách (Giá sách x 2.0). |
| `BROKEN_BOOK_COEFFICIENT` | 0.5 | Hệ số phạt khi làm hỏng/rách sách (Giá sách x 0.5). |

## 2. Các tác vụ tự động (Jobs)

Hệ thống hiện có 5 tác vụ chính chạy theo lịch trình:

### [Job 1] Cập nhật phiếu quá hạn
- **Thời gian**: Chạy vào **00:00** hàng ngày.
- **Logic**: Kiểm tra tất cả phiếu mượn có trạng thái `DANG_MUON`. Nếu `ngày hiện tại > hạn trả`, tự động chuyển sang trạng thái `QUA_HAN`.

### [Job 2] Tính phạt tự động & Gửi Email
- **Thời gian**: Chạy vào **00:05** hàng ngày.
- **Logic**: 
  1. Tính số tiền phạt dựa trên số ngày quá hạn.
  2. Tạo bản ghi vi phạm mới trong bảng `vi_pham_phat`.
  3. **Tự động gửi email** thông báo cho độc giả về số ngày quá hạn và số tiền phạt hiện tại.

### [Job 3] Email nhắc nhở sắp đến hạn
- **Thời gian**: Chạy vào **08:00** hàng ngày.
- **Logic**: Tìm các phiếu mượn sẽ hết hạn sau **2 ngày** nữa và gửi email nhắc nhở độc giả trả sách đúng hạn.

### [Job 4] Tự động khóa thẻ
- **Thời gian**: Chạy mỗi **6 tiếng** một lần.
- **Logic**: Nếu độc giả có bất kỳ vi phạm nào chưa thanh toán (`chua_thanh_toan`), hệ thống tự động khóa thẻ thư viện và gửi email thông báo.

### [Job 5] Hủy đặt trước hết hạn
- **Thời gian**: Chạy vào **00:00 Thứ Hai** hàng tuần.
- **Logic**: Hủy các yêu cầu đặt trước sách đã quá 7 ngày mà độc giả chưa đến nhận.

## 3. Logic phạt theo giá sách (Mất/Hỏng)

Trong Router `vi_pham.py`, hệ thống tự động nhận diện lý do vi phạm để áp dụng mức phạt:

- **Mất sách**: Nếu lý do có chứa từ "mất" (không dấu hoặc có dấu), tiền phạt = `Giá sách * LOST_BOOK_COEFFICIENT`.
- **Hỏng/Rách**: Nếu lý do có chứa từ "hỏng" hoặc "rách", tiền phạt = `Giá sách * BROKEN_BOOK_COEFFICIENT`.
- **Lưu ý**: Cần nhập đúng giá tiền trong thông tin Tài liệu để hệ thống tính toán chính xác.

## 4. Cách khởi chạy

Hệ thống tự động hóa được tích hợp sẵn vào file `main.py`. Khi bạn khởi chạy backend bằng `uvicorn`, Scheduler sẽ tự động bắt đầu:

```powershell
# Chạy backend
cd backend
uvicorn main:app --reload
```

Thông báo `[OK] Scheduler started with 5 automation jobs` sẽ xuất hiện ở console nếu khởi chạy thành công.
