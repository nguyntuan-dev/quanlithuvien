# Kiểm thử (Testing)

Tất cả script Python chạy từ thư mục `backend/` (đã cấu hình `DATABASE_URL` nếu khác mặc định).

## Điều kiện chung

| Loại | Yêu cầu |
|------|----------|
| `test_db.py` | PostgreSQL chạy, bảng đã tạo (thường qua `uvicorn` startup hoặc migrate thủ công) |
| `test_crud.py`, `test_api_extended.py`, `test_security.py` | Backend **đang chạy** tại `http://127.0.0.1:8000` (hoặc sửa biến `base` trong từng file) |
| Build frontend | Node.js, `npm install` đã chạy trong `frontend/` |

## 1. Kiểm tra kết nối database

```powershell
cd backend
py -3 test_db.py
```

Kết nối engine, liệt kê bảng, đếm số bản ghi mẫu (`TaiLieu`, `DocGia`, `NhanVien`).

## 2. Kiểm thử CRUD + luồng nghiệp vụ cốt lõi (`test_crud.py`)

Chạy **sau** khi bật API:

```powershell
py -3 -m uvicorn main:app --host 127.0.0.1 --port 8000
```

Terminal khác:

```powershell
cd backend
py -3 test_crud.py
```

Luồng gồm: đăng nhập admin → tạo/sửa tài liệu test → độc giả → phiếu mượn → trả sách → đặt trước/hủy → thống kê tổng quan → dọn dữ liệu test trong DB.

## 3. Kiểm thử mở rộng (`test_api_extended.py`)

Bao phủ thêm: thống kê phụ, meta tài liệu, bản sao, vi phạm + thanh toán, gia hạn, nhân viên (admin), hệ thống (cấu hình, audit, backup/restore), độc giả (yêu thích, đổi mật khẩu cá nhân).

```powershell
cd backend
py -3 test_api_extended.py
```

**Lưu ý Windows:** Một số dòng log có thể hiển thị ký tự thay thế nếu console không UTF-8; mã HTTP vẫn đúng.

## 4. Kiểm thử bảo mật (`test_security.py`)

Kiểm tra 401/403/422 theo kịch bản phân quyền và in **WARN** cho các route mở (không auth). Chứng minh rủi ro `POST /api/auth/doi-mat-khau` (xem [SECURITY.md](./SECURITY.md)).

```powershell
cd backend
py -3 test_security.py
```

## 5. Smoke test frontend (build production)

```powershell
cd frontend
npm run build
```

Dự án chưa cấu hình Vitest/Jest; build Vite đóng vai trò kiểm tra biên dịch.

## 6. File khác (`test_conn.py`)

Script độc lập kiểm tra chuỗi kết nối PostgreSQL cứng trong file — chỉ dùng khi bạn chủ động chỉnh URL trong file cho môi trường dev.

## Gợi ý chạy full nhanh (PowerShell)

```powershell
# Terminal 1
cd backend
py -3 -m uvicorn main:app --host 127.0.0.1 --port 8000

# Terminal 2
cd backend
py -3 test_db.py
py -3 test_crud.py
py -3 test_api_extended.py
py -3 test_security.py

cd ..\frontend
npm run build
```
