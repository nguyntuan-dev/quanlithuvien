# Quy trình Đặt trước & Duyệt trả sách

Tài liệu mô tả hai quy trình phê duyệt trong hệ thống Thư Viện Pro:
1. Độc giả **đặt trước** sách → Thủ thư **duyệt đặt trước**
2. Độc giả **yêu cầu trả** sách → Thủ thư **duyệt trả**

---

## 1. Quy trình Đặt trước tài liệu

### Luồng hoạt động

```
Độc giả đặt chỗ ──→ [cho_xu_ly] ──→ Thủ thư duyệt ──→ [da_duyet]
                                  └─→ Thủ thư từ chối ─→ [da_huy]
                                  
Sau khi mượn sách ──→ Hệ thống tự cập nhật ──→ [da_nhan_sach]
```

### Bước 1: Độc giả đặt chỗ
- Tra cứu sách trong kho (Catalog), nhấn **"Đặt chỗ"**.
- Hệ thống tạo yêu cầu với trạng thái `cho_xu_ly`.

### Bước 2: Thủ thư phê duyệt
- Vào **"Đặt trước"** hoặc xem thống kê **"Đang chờ duyệt"** tại Dashboard.
- **Duyệt**: Sách có sẵn → nhấn "Duyệt" → `da_duyet`.
- **Từ chối**: Không đủ điều kiện → nhấn "Từ chối" → `da_huy`.

### Bước 3: Độc giả nhận sách
- Độc giả đến thư viện, thủ thư tạo **Phiếu mượn**.
- Hệ thống **tự động** chuyển đặt trước sang `da_nhan_sach`.

### Trạng thái đặt trước

| Mã trạng thái    | Hiển thị      | Ý nghĩa |
|-------------------|---------------|---------|
| `cho_xu_ly`       | Chờ duyệt     | Yêu cầu mới, đang chờ thủ thư xử lý |
| `da_duyet`        | Đã duyệt      | Thủ thư xác nhận giữ sách cho độc giả |
| `da_huy`          | Đã hủy        | Bị từ chối hoặc độc giả tự hủy |
| `da_nhan_sach`    | Đã nhận sách   | Đã tạo phiếu mượn, hoàn tất quy trình |

### API đặt trước

| Method | Endpoint | Mô tả | Quyền |
|--------|----------|-------|-------|
| `GET`  | `/api/dat-truoc/` | Danh sách (lọc `ma_doc_gia`) | Staff / Reader |
| `POST` | `/api/dat-truoc/` | Tạo yêu cầu đặt chỗ | Reader |
| `PUT`  | `/api/dat-truoc/{ma}/duyet` | Phê duyệt yêu cầu | Staff |
| `PUT`  | `/api/dat-truoc/{ma}/huy` | Hủy / Từ chối | Staff / Reader |

---

## 2. Quy trình Duyệt trả sách

### Luồng hoạt động

```
Độc giả nhấn "Yêu cầu trả" ──→ [cho_tra] ──→ Thủ thư duyệt trả ──→ [da_tra]
```

### Bước 1: Độc giả gửi yêu cầu trả
- Vào **"Sách của tôi"**, tìm sách đang mượn.
- Nhấn **"Yêu cầu trả"** → trạng thái chuyển sang `cho_tra`.
- Hiển thị thông báo **"Đang chờ thủ thư duyệt"**.

### Bước 2: Thủ thư duyệt trả
- Vào **"Mượn / Trả"**, chọn tab **"Chờ trả"**.
- Kiểm tra tình trạng sách thực tế, chọn tình trạng (Tốt / Hỏng / Mất).
- Nhấn **"Duyệt trả"** → trạng thái chuyển sang `da_tra`.
- Nếu sách bị hỏng/mất, hệ thống tự động tạo phiếu phạt.

### Trạng thái phiếu mượn

| Mã trạng thái | Hiển thị        | Ý nghĩa |
|---------------|-----------------|---------|
| `dang_muon`   | Đang mượn        | Sách đang được mượn |
| `cho_tra`     | Chờ duyệt trả   | Độc giả đã yêu cầu trả, chờ thủ thư xác nhận |
| `da_tra`      | Đã trả           | Thủ thư xác nhận nhận lại sách |
| `qua_han`     | Quá hạn          | Quá hạn trả sách |

### API mượn/trả

| Method | Endpoint | Mô tả | Quyền |
|--------|----------|-------|-------|
| `PUT`  | `/api/muon-tra/{ma}/yeu-cau-tra` | Độc giả yêu cầu trả sách | Reader |
| `POST` | `/api/muon-tra/tra-sach` | Thủ thư duyệt trả (chọn tình trạng) | Staff |
| `PUT`  | `/api/muon-tra/{ma}/gia-han` | Gia hạn phiếu mượn | Staff / Reader |

---

## 3. Giao diện người dùng

### Phía độc giả (Reader)
- **Tra cứu sách** → Nhấn "Đặt chỗ"
- **Sách của tôi** → Xem đặt trước + lịch sử mượn, nhấn "Yêu cầu trả" hoặc "Hủy đặt"

### Phía thủ thư (Staff)
- **Dashboard** → Thẻ "Đang chờ duyệt" hiển thị số đặt trước cần xử lý
- **Đặt trước** → Duyệt / Từ chối yêu cầu đặt sách
- **Mượn / Trả** → Tab "Chờ trả" hiển thị các yêu cầu trả sách cần duyệt

---

> [!TIP]
> Hệ thống có job tự động (Task 5 trong [AUTOMATION.md](./AUTOMATION.md)) để tự động hủy các yêu cầu đặt trước đã quá hạn nhận sách (sau 7 ngày kể từ khi duyệt mà độc giả chưa đến lấy).
