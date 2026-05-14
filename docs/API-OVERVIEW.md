# API — Tổng quan

Base URL mặc định dev: `http://127.0.0.1:8000`  
Prefix API: `/api`

Tài liệu tương tác đầy đủ: **http://localhost:8000/docs** (Swagger), **/redoc**.

## Header chung

| Header | Khi nào cần |
|--------|-------------|
| `Content-Type: application/json` | Body JSON |
| `Authorization: Bearer <token>` | Sau khi đăng nhập nhân viên hoặc độc giả |

## Nhóm endpoint (rút gọn)

### Xác thực — `/api/auth`

| Phương thức | Đường dẫn | Ghi chú |
|-------------|-----------|---------|
| POST | `/dang-nhap` | Nhân viên |
| POST | `/doc-gia/dang-nhap` | Độc giả |
| POST | `/doc-gia/dang-ky` | Đăng ký + OTP (xem schema) |
| POST | `/doc-gia/send-otp` | Gửi OTP |
| POST | `/doi-mat-khau` | Đổi mật theo email — **rủi ro bảo mật**, xem SECURITY.md |
| POST | `/ca-nhan/doi-mat-khau` | Đổi mật khi đã có token |
| PUT | `/ca-nhan/doc-gia`, `/ca-nhan/nhan-vien` | Cập nhật hồ sơ |
| POST | `/tao-tai-khoan` | Tạo nhân viên — **chỉ admin** |

### Tài liệu — `/api/tai-lieu`

CRUD tài liệu, meta tác giả / thể loại / NXB, quản lý **bản sao** (`/ban-sao/`).

### Độc giả — `/api/doc-gia`

Danh sách, chi tiết, tạo/sửa/xóa (hiện **không** bắt buộc token ở router).

### Mượn / trả — `/api/muon-tra`

| Phương thức | Đường dẫn | Mô tả | Quyền |
|-------------|-----------|-------|-------|
| GET | `/` | Danh sách phiếu mượn (lọc `trang_thai`, `ma_doc_gia`) | Staff |
| GET | `/{ma}` | Chi tiết phiếu mượn | Staff / Reader |
| GET | `/lich-su/{ma_doc_gia}` | Lịch sử mượn của độc giả | Reader |
| GET | `/qua-han` | Danh sách phiếu quá hạn | Staff |
| POST | `/` | Lập phiếu mượn mới | Staff |
| PUT | `/{ma}/gia-han` | Gia hạn phiếu mượn | Staff / Reader |
| PUT | `/{ma}/yeu-cau-tra` | Độc giả yêu cầu trả sách (`cho_tra`) | Reader |
| POST | `/tra-sach` | Thủ thư duyệt trả sách (chọn tình trạng) | Staff |

### Đặt trước — `/api/dat-truoc`

| Phương thức | Đường dẫn | Mô tả | Quyền |
|-------------|-----------|-------|-------|
| GET | `/` | Danh sách đặt trước (lọc `ma_doc_gia`) | Staff/Reader |
| POST | `/` | Tạo yêu cầu đặt chỗ | Reader |
| PUT | `/{ma}/duyet` | Phê duyệt yêu cầu | Staff |
| PUT | `/{ma}/huy` | Hủy/Từ chối yêu cầu | Staff/Reader |

### Vi phạm — `/api/vi-pham/vi-pham/`

(Lưu ý: router con có prefix `vi-pham` — đường dẫn đầy đủ chứa hai đoạn `vi-pham`.)

### Nhân viên — `/api/nhan-vien`

**Admin:** danh sách, chi tiết, thêm, xóa.

### Thống kê — `/api/thong-ke`

`tong-quan`, `muon-theo-thang`, `top-tai-lieu` (một số endpoint không yêu cầu auth — phù hợp dashboard mở; cần xem lại nếu public).

### Hệ thống — `/api/he-thong`

**Admin:** `cau-hinh`, `audit-log`, `backup`, `restore`.

### Yêu thích — `/api/yeu-thich`

**Độc giả đã đăng nhập:** danh sách, thêm, xóa.

## Frontend (`frontend/src/services/api.js`)

`baseURL` mặc định trỏ `http://127.0.0.1:8000/api` — đổi qua biến môi trường build nếu triển khai xa máy dev.
