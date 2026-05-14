-- ============================================================
-- SEED DATA - Hệ thống Quản lý Thư viện (Sạch 100% UTF-8)
-- ============================================================

SET client_encoding = 'UTF8';

-- Thể loại
INSERT INTO the_loai (ma_the_loai, ten_the_loai) VALUES
  ('CNTT',    'Công nghệ thông tin'),
  ('TOAN',    'Toán học'),
  ('VHNT',    'Văn học - Nghệ thuật'),
  ('KINHTE',  'Kinh tế'),
  ('KTHUAT',  'Kỹ thuật'),
  ('NGOAINGU','Ngoại ngữ'),
  ('LICHSU',  'Lịch sử'),
  ('KHTN',    'Khoa học tự nhiên'),
  ('TRIETON', 'Triết học / Tôn giáo'),
  ('TAMLY',   'Tâm lý học / Phát triển bản thân'),
  ('THIEUNHI','Truyện thiếu nhi / Thiếu niên'),
  ('AMTHUC',  'Sách nấu ăn / Ẩm thực'),
  ('DULICH',  'Du lịch / Địa lý'),
  ('HOCTHUAT','Sách tham khảo / Học thuật chuyên ngành'),
  ('NGHETHUAT','Nghệ thuật & Thiết kế')
ON CONFLICT (ma_the_loai) DO UPDATE SET ten_the_loai = EXCLUDED.ten_the_loai;

-- Tác giả
INSERT INTO tac_gia (ma_tac_gia, ten_tac_gia) VALUES
  ('TG001', 'Nguyễn Văn Anh'),
  ('TG002', 'Trần Quốc Bảo'),
  ('TG003', 'Lê Minh Cường'),
  ('TG004', 'Phạm Thị Dung'),
  ('TG005', 'Hoàng Quang Đức')
ON CONFLICT (ma_tac_gia) DO UPDATE SET ten_tac_gia = EXCLUDED.ten_tac_gia;

-- Nhà xuất bản
INSERT INTO nha_xuat_ban (ma_nxb, ten_nxb, dia_chi) VALUES
  ('NXB001', 'NXB Khoa học & Kỹ thuật',     'Hà Nội'),
  ('NXB002', 'NXB Đại học Quốc gia Hà Nội', 'Hà Nội'),
  ('NXB003', 'NXB Thống kê',                'Hà Nội'),
  ('NXB004', 'NXB Giáo dục Việt Nam',       'Hà Nội')
ON CONFLICT (ma_nxb) DO UPDATE SET ten_nxb = EXCLUDED.ten_nxb, dia_chi = EXCLUDED.dia_chi;

-- Tài liệu mẫu (Thêm tinh_trang = 'CO_SAN' để tránh lỗi 500)
INSERT INTO tai_lieu (ma_tai_lieu, ten_tai_lieu, nam_xuat_ban, so_luong, gia, vi_tri, ma_tac_gia, ma_the_loai, ma_nxb, tinh_trang) VALUES
  ('TL001', 'Lập trình Python cơ bản', 2022, 5, 120000, 'Kệ A1', 'TG001', 'CNTT',   'NXB001', 'CO_SAN'),
  ('TL002', 'Giải tích 1',             2020, 3,  95000, 'Kệ B2', 'TG002', 'TOAN',   'NXB002', 'CO_SAN'),
  ('TL003', 'Cơ sở dữ liệu',          2021, 7, 145000, 'Kệ A2', 'TG003', 'CNTT',   'NXB001', 'CO_SAN'),
  ('TL004', 'Kinh tế vi mô',          2023, 4, 110000, 'Kệ C1', 'TG004', 'KINHTE', 'NXB003', 'CO_SAN'),
  ('TL005', 'Mạng máy tính',          2022, 6, 135000, 'Kệ A3', 'TG001', 'CNTT',   'NXB001', 'CO_SAN'),
  ('TL006', 'Truyện Kiều',            1820, 8,  80000, 'Kệ D1', 'TG005', 'VHNT',   'NXB004', 'CO_SAN'),
  ('TL007', 'Lập trình Java nâng cao', 2023, 3, 150000, 'Kệ A4', 'TG003', 'CNTT',  'NXB001', 'CO_SAN'),
  ('TL008', 'Xác suất thống kê',      2021, 5, 100000, 'Kệ B3', 'TG002', 'TOAN',   'NXB002', 'CO_SAN')
ON CONFLICT (ma_tai_lieu) DO UPDATE SET 
  ten_tai_lieu = EXCLUDED.ten_tai_lieu, 
  tinh_trang = EXCLUDED.tinh_trang;

-- Nhân viên (mật khẩu: 18112006)
INSERT INTO nhan_vien (ma_nhan_vien, ho_ten, chuc_vu, email, mat_khau_hash, la_admin) VALUES
  ('NV000001', 'Quản trị viên',  'Admin',   'admin@thuvien.vn', encode(sha256('18112006'::bytea), 'hex'), true),
  ('NV000002', 'Nguyễn Thị Lan', 'Thủ thư', 'lan@thuvien.vn',   encode(sha256('18112006'::bytea), 'hex'), false)
ON CONFLICT (ma_nhan_vien) DO UPDATE SET ho_ten = EXCLUDED.ho_ten;

-- Độc giả mẫu
INSERT INTO doc_gia (ma_doc_gia, ho_ten, ngay_sinh, gioi_tinh, so_dien_thoai, email, trang_thai_the) VALUES
  ('DG000001', 'Nguyễn Thị Hoa', '2002-03-15', 'NU',  '0912345678', 'hoa@email.com', 'CON_HIEU_LUC'),
  ('DG000002', 'Trần Minh Đức',  '2001-07-22', 'NAM', '0987654321', 'duc@email.com', 'CON_HIEU_LUC'),
  ('DG000003', 'Phạm Thị Thu',   '2003-11-08', 'NU',  '0966111222', 'thu@email.com', 'BI_KHOA'),
  ('DG000004', 'Lê Quang Huy',   '2002-05-30', 'NAM', '0355999888', 'huy@email.com', 'HET_HAN')
ON CONFLICT (ma_doc_gia) DO UPDATE SET ho_ten = EXCLUDED.ho_ten, trang_thai_the = EXCLUDED.trang_thai_the;

-- Thẻ thư viện mẫu
INSERT INTO the_thu_vien (ma_the, ngay_cap, ngay_het_han, loai_the, trang_thai, ma_doc_gia) VALUES
  ('THE0001', '2024-01-10', '2026-01-10', 'Thẻ sinh viên (1 năm)', 'CON_HIEU_LUC', 'DG000001'),
  ('THE0002', '2024-02-15', '2026-02-15', 'Thẻ sinh viên (1 năm)', 'CON_HIEU_LUC', 'DG000002'),
  ('THE0003', '2023-05-01', '2024-05-01', 'Thẻ sinh viên (1 năm)', 'BI_KHOA',      'DG000003'),
  ('THE0004', '2023-03-20', '2024-03-20', 'Thẻ sinh viên (1 năm)', 'HET_HAN',      'DG000004')
ON CONFLICT (ma_the) DO NOTHING;

SELECT 'Seed data imported successfully!' as status;
