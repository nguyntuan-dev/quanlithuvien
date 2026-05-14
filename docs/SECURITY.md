# Bảo mật (Security)

Tài liệu mô tả **trạng thái hiện tại** của backend và các rủi ro cần biết trước khi triển khai thật.

## Mô hình xác thực

- **Nhân viên:** `POST /api/auth/dang-nhap` → `access_token` (lưu trong bộ nhớ process: dict `TOKENS` trong `routers/auth.py`).
- **Độc giả:** `POST /api/auth/doc-gia/dang-nhap` → token tương tự, phân loại `doc_gia` trong cùng dict.
- Header: `Authorization: Bearer <token>`.

Token **không** phải JWT có hạn hạn; **mất khi restart process** server.

## Phân quyền (tóm tắt)

| Vùng | Ai được phép |
|------|----------------|
| `/api/he-thong/*`, `GET/POST/DELETE /api/nhan-vien/*`, `POST /api/auth/tao-tai-khoan` | Nhân viên **admin** (`la_admin = true`) |
| `/api/yeu-thich/*`, `PUT /api/auth/ca-nhan/doc-gia` | Độc giả đã đăng nhập (token độc giả) |
| `POST /api/auth/ca-nhan/doi-mat-khau` | Bất kỳ ai có token hợp lệ (nhân viên hoặc độc giả), kèm mật khẩu cũ/mới trong body |

Các router **tài liệu, độc giả, mượn-trả, đặt trước, vi phạm, thống kê** phần lớn **không** gắn `Depends(get_current_nhan_vien)` — nghĩa là client có thể gọi trực tiếp API mà không cần đăng nhập nhân viên. Điều này phù hợp demo / nội bộ tin cậy, **không** phù hợp Internet công khai.

## Mật khẩu

- Lưu dạng **SHA-256** (hex), **không salt** — chống rainbow table kém hơn bcrypt/argon2.
- Khuyến nghị production: **argon2** hoặc **bcrypt** + chính sách độ dài mật khẩu.

## Rủi ro nghiêm trọng: đổi mật khẩu công khai

`POST /api/auth/doi-mat-khau` nhận `email` + `mat_khau_moi` và **ghi đè mật khẩu** nếu tìm thấy tài khoản (độc giả hoặc nhân viên) — **không** yêu cầu mật khẩu cũ hay OTP.

- Ai biết email (và API lộ ra ngoài) có thể chiếm tài khoản.
- Frontend có thể dùng endpoint này cho luồng “quên mật khẩu” đơn giản — cần thay bằng OTP email, magic link có chữ ký, hoặc **tắt** endpoint trên môi trường production.

Luồng an toàn hơn cho user đã đăng nhập: `POST /api/auth/ca-nhan/doi-mat-khau` (có `mat_khau_cu`).

## SMTP / OTP

- Gửi OTP đăng ký: biến môi trường `SMTP_*`. Không log mật khẩu SMTP ra console (đã chuyển sang `logging`).
- OTP lưu trong bộ nhớ `OTP_CODES` — phù hợp dev; production nên giới hạn tốc độ gửi (rate limit) và theo dõi abuse.

## CORS

`main.py` cấu hình `allow_origins` cho localhost — trước khi public domain, cần thu hẹp origin và xem xét `allow_credentials`.

## Kiểm thử tự động

Chạy `test_security.py` (xem [TESTING.md](./TESTING.md)) để xác nhận 401/403 trên route được bảo vệ và xem cảnh báo WARN cho surface API mở.

## Checklist trước production (gợi ý)

1. Bọc **mọi thao tác ghi** (POST/PUT/DELETE) bằng xác thực nhân viên (hoặc tách API public chỉ đọc).
2. Thay thế / vô hiệu hóa `doi-mat-khau` công khai; dùng reset có bằng chứng sở hữu.
3. Hash mật khẩu bằng thuật toán chuyên dụng + salt/pepper.
4. Token có thời hạn (JWT + refresh) hoặc session server có TTL.
5. HTTPS, reverse proxy, rate limit, log audit không chứa secret.
