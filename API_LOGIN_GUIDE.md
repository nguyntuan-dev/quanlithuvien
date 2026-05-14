# 🔐 Hướng dẫn Đăng nhập Hệ thống Quản lý Thư viện

## ⚠️ Frontend KHÔNG CÓ form login hiển thị

Giao diện web chỉ chấp nhận token JWT được gửi qua API. Điều này giúp:
- ✅ Bảo mật cao hơn (không lộ tài khoản qua giao diện)
- ✅ Hỗ trợ login từ nhiều ứng dụng khác nhau
- ✅ Dễ kiểm soát phiên đăng nhập

---

## 📱 Cách đăng nhập

### 1️⃣ Gửi request POST tới API

**URL:** `http://localhost:8000/api/auth/dang-nhap`

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "email": "admin@thuvien.vn",
  "mat_khau": "18112006"
}
```

### 2️⃣ API trả về response

**Success (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "nhan_vien": {
    "ma_nhan_vien": "NV000001",
    "ho_ten": "Quản trị viên",
    "email": "admin@thuvien.vn",
    "la_admin": true
  }
}
```

### 3️⃣ Lưu token và truy cập frontend

Lưu `access_token` vào localStorage:
```javascript
localStorage.setItem('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...');
localStorage.setItem('user', JSON.stringify({...}));
```

Rồi truy cập: **`http://localhost:5173`**

Frontend sẽ tự động sử dụng token để gọi API.

---

## 🛠️ Tools để test API

### Option 1: Postman / Thunder Client
1. Tạo request POST
2. URL: `http://localhost:8000/api/auth/dang-nhap`
3. Body (raw JSON):
```json
{
  "email": "admin@thuvien.vn",
  "mat_khau": "18112006"
}
```
4. Click Send → copy token

### Option 2: cURL
```bash
curl -X POST http://localhost:8000/api/auth/dang-nhap \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@thuvien.vn",
    "mat_khau": "18112006"
  }'
```

### Option 3: Python
```python
import requests

response = requests.post(
    "http://localhost:8000/api/auth/dang-nhap",
    json={
        "email": "admin@thuvien.vn",
        "mat_khau": "18112006"
    }
)

token = response.json()["access_token"]
print(token)
```

---

## 👥 Tài khoản mặc định

| Email | Mật khẩu | Quyền |
|-------|----------|-------|
| admin@thuvien.vn | 18112006 | Admin |
| lan@thuvien.vn | 18112006 | Thủ thư |

---

## 🔗 API Endpoints khác

Sau khi lấy token, dùng nó trong header để call các API khác:

```bash
curl -X GET http://localhost:8000/api/tai-lieu/ \
  -H "Authorization: Bearer {token}"
```

---

## 📝 Ghi chú

- Token hết hạn sau 24 giờ (cấu hình trong backend)
- Mỗi thiết bị/app khác nhau sẽ có token riêng
- Để logout: xóa token khỏi localStorage
