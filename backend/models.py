from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, Numeric, Enum, Text, Boolean, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class TrangThaiTaiLieu(str, enum.Enum):
    CO_SAN      = "CO_SAN"
    DANG_MUON   = "DANG_MUON"
    DAT_TRUOC   = "DAT_TRUOC"
    BAO_TRI     = "BAO_TRI"
    THANH_LY    = "THANH_LY"

class TrangThaiThe(str, enum.Enum):
    CON_HIEU_LUC = "CON_HIEU_LUC"
    HET_HAN      = "HET_HAN"
    BI_KHOA      = "BI_KHOA"

class TrangThaiPhieu(str, enum.Enum):
    DANG_MUON    = "DANG_MUON"
    CHO_TRA      = "CHO_TRA"
    DA_TRA       = "DA_TRA"
    QUA_HAN      = "QUA_HAN"

class TrangThaiPhat(str, enum.Enum):
    CHUA_THANH_TOAN = "CHUA_THANH_TOAN"
    DA_THANH_TOAN   = "DA_THANH_TOAN"

class GioiTinh(str, enum.Enum):
    NAM  = "NAM"
    NU   = "NU"
    KHAC = "KHAC"

# ── Thể loại ─────────────────────────────────────────────────────────────────
class TheLoai(Base):
    __tablename__ = "the_loai"
    ma_the_loai  = Column(String(20),  primary_key=True)
    ten_the_loai = Column(String(100), nullable=False)
    tai_lieu     = relationship("TaiLieu", back_populates="the_loai")

# ── Tác giả ──────────────────────────────────────────────────────────────────
class TacGia(Base):
    __tablename__ = "tac_gia"
    ma_tac_gia  = Column(String(20),  primary_key=True)
    ten_tac_gia = Column(String(150), nullable=False)
    ghi_chu     = Column(Text)
    tai_lieu    = relationship("TaiLieu", back_populates="tac_gia")

# ── Nhà xuất bản ─────────────────────────────────────────────────────────────
class NhaXuatBan(Base):
    __tablename__ = "nha_xuat_ban"
    ma_nxb       = Column(String(20),  primary_key=True)
    ten_nxb      = Column(String(150), nullable=False)
    dia_chi      = Column(String(255))
    so_dien_thoai = Column(String(20))
    tai_lieu     = relationship("TaiLieu", back_populates="nha_xuat_ban")

# ── Tài liệu ─────────────────────────────────────────────────────────────────
class TaiLieu(Base):
    __tablename__ = "tai_lieu"
    ma_tai_lieu  = Column(String(20),  primary_key=True)
    ten_tai_lieu = Column(String(255), nullable=False)
    nam_xuat_ban = Column(Integer)
    so_luong     = Column(Integer, default=1)
    gia          = Column(Numeric(12, 0), default=0)
    anh_bia      = Column(Text)
    vi_tri       = Column(String(100))
    tinh_trang   = Column(Enum(TrangThaiTaiLieu), default=TrangThaiTaiLieu.CO_SAN)
    mo_ta        = Column(Text)
    ma_tac_gia   = Column(String(20), ForeignKey("tac_gia.ma_tac_gia"))
    ma_the_loai  = Column(String(20), ForeignKey("the_loai.ma_the_loai"))
    ma_nxb       = Column(String(20), ForeignKey("nha_xuat_ban.ma_nxb"))
    created_at   = Column(DateTime(timezone=True), server_default=func.now())
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

    tac_gia      = relationship("TacGia",      back_populates="tai_lieu")
    the_loai     = relationship("TheLoai",     back_populates="tai_lieu")
    nha_xuat_ban = relationship("NhaXuatBan",  back_populates="tai_lieu")
    chi_tiet_phieu_muon = relationship("ChiTietPhieuMuon", back_populates="tai_lieu")
    dat_truoc    = relationship("DatTruoc",    back_populates="tai_lieu")
    ban_sao      = relationship("BanSaoTaiLieu", back_populates="tai_lieu")

class BanSaoTaiLieu(Base):
    __tablename__ = "ban_sao_tai_lieu"
    ma_ban_sao   = Column(String(30), primary_key=True)
    ma_tai_lieu  = Column(String(20), ForeignKey("tai_lieu.ma_tai_lieu"))
    ma_vach      = Column(String(50), unique=True)
    tinh_trang   = Column(Enum(TrangThaiTaiLieu), default=TrangThaiTaiLieu.CO_SAN)
    ghi_chu      = Column(Text)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    tai_lieu     = relationship("TaiLieu", back_populates="ban_sao")

# ── Độc giả ──────────────────────────────────────────────────────────────────
class DocGia(Base):
    __tablename__ = "doc_gia"
    ma_doc_gia   = Column(String(20),  primary_key=True)
    ho_ten       = Column(String(150), nullable=False)
    ngay_sinh    = Column(Date)
    gioi_tinh    = Column(Enum(GioiTinh))
    dia_chi      = Column(String(255))
    so_dien_thoai = Column(String(20))
    email        = Column(String(150))
    mat_khau_hash = Column(String(255))
    trang_thai_the = Column(Enum(TrangThaiThe), default=TrangThaiThe.CON_HIEU_LUC)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    the_thu_vien = relationship("TheThuvien",   back_populates="doc_gia", uselist=False)
    phieu_muon   = relationship("PhieuMuon",    back_populates="doc_gia")
    dat_truoc    = relationship("DatTruoc",     back_populates="doc_gia")

# ── Thẻ thư viện ─────────────────────────────────────────────────────────────
class TheThuvien(Base):
    __tablename__ = "the_thu_vien"
    ma_the       = Column(String(20),  primary_key=True)
    ngay_cap     = Column(Date,        nullable=False)
    ngay_het_han = Column(Date,        nullable=False)
    loai_the     = Column(String(50))
    trang_thai   = Column(Enum(TrangThaiThe), default=TrangThaiThe.CON_HIEU_LUC)
    ma_doc_gia   = Column(String(20),  ForeignKey("doc_gia.ma_doc_gia"), unique=True)
    doc_gia      = relationship("DocGia", back_populates="the_thu_vien")

# ── Nhân viên ─────────────────────────────────────────────────────────────────
class NhanVien(Base):
    __tablename__ = "nhan_vien"
    ma_nhan_vien  = Column(String(20),  primary_key=True)
    ho_ten        = Column(String(150), nullable=False)
    chuc_vu       = Column(String(100))
    so_dien_thoai = Column(String(20))
    email         = Column(String(150), unique=True)
    mat_khau_hash = Column(String(255))
    la_admin      = Column(Boolean, default=False)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    phieu_muon    = relationship("PhieuMuon", back_populates="nhan_vien")

# ── Phiếu mượn ───────────────────────────────────────────────────────────────
class PhieuMuon(Base):
    __tablename__ = "phieu_muon"
    ma_phieu_muon = Column(String(30),  primary_key=True)
    ngay_muon     = Column(Date,        nullable=False)
    han_tra       = Column(Date,        nullable=False)
    trang_thai    = Column(Enum(TrangThaiPhieu), default=TrangThaiPhieu.DANG_MUON)
    ghi_chu       = Column(Text)
    ma_doc_gia    = Column(String(20),  ForeignKey("doc_gia.ma_doc_gia"))
    ma_nhan_vien  = Column(String(20),  ForeignKey("nhan_vien.ma_nhan_vien"))
    created_at    = Column(DateTime(timezone=True), server_default=func.now())

    doc_gia       = relationship("DocGia",     back_populates="phieu_muon")
    nhan_vien     = relationship("NhanVien",   back_populates="phieu_muon")
    chi_tiet      = relationship("ChiTietPhieuMuon", back_populates="phieu_muon")
    vi_pham_phat  = relationship("ViPhamPhat", back_populates="phieu_muon")

# ── Chi tiết phiếu mượn ───────────────────────────────────────────────────────
class ChiTietPhieuMuon(Base):
    __tablename__ = "ct_phieu_muon"
    id            = Column(Integer, primary_key=True, autoincrement=True)
    ma_phieu_muon = Column(String(30), ForeignKey("phieu_muon.ma_phieu_muon"))
    ma_tai_lieu   = Column(String(20), ForeignKey("tai_lieu.ma_tai_lieu"))
    so_luong      = Column(Integer, default=1)
    ngay_tra      = Column(Date)
    tinh_trang_tra = Column(String(100))

    phieu_muon    = relationship("PhieuMuon",  back_populates="chi_tiet")
    tai_lieu      = relationship("TaiLieu",    back_populates="chi_tiet_phieu_muon")

# ── Đặt trước ─────────────────────────────────────────────────────────────────
class DatTruoc(Base):
    __tablename__ = "dat_truoc"
    ma_dat_truoc  = Column(String(30),  primary_key=True)
    ngay_dat      = Column(DateTime(timezone=True), server_default=func.now())
    trang_thai    = Column(String(50), default="cho_xu_ly")
    ma_doc_gia    = Column(String(20), ForeignKey("doc_gia.ma_doc_gia"))
    ma_tai_lieu   = Column(String(20), ForeignKey("tai_lieu.ma_tai_lieu"))

    doc_gia       = relationship("DocGia",   back_populates="dat_truoc")
    tai_lieu      = relationship("TaiLieu",  back_populates="dat_truoc")

# ── Vi phạm & Phạt ───────────────────────────────────────────────────────────
class ViPhamPhat(Base):
    __tablename__ = "vi_pham_phat"
    ma_phat           = Column(String(30),  primary_key=True)
    ly_do_phat        = Column(String(255), nullable=False)
    so_tien           = Column(Numeric(12, 0), nullable=False)
    trang_thai_thanh_toan = Column(Enum(TrangThaiPhat), default=TrangThaiPhat.CHUA_THANH_TOAN)
    ngay_phat         = Column(DateTime(timezone=True), server_default=func.now())
    ngay_thanh_toan   = Column(DateTime(timezone=True))
    ma_phieu_muon     = Column(String(30), ForeignKey("phieu_muon.ma_phieu_muon"))
    phieu_muon        = relationship("PhieuMuon", back_populates="vi_pham_phat")

class CauHinhHeThong(Base):
    __tablename__ = "cau_hinh_he_thong"
    khoa         = Column(String(100), primary_key=True)
    gia_tri      = Column(String(255), nullable=False)
    mo_ta        = Column(String(255))
    updated_at   = Column(DateTime(timezone=True), onupdate=func.now())

class AuditLog(Base):
    __tablename__ = "audit_log"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    hanh_dong    = Column(String(100), nullable=False)
    doi_tuong    = Column(String(100))
    ma_doi_tuong = Column(String(100))
    nguoi_thuc_hien = Column(String(150))
    chi_tiet     = Column(Text)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

# ── Sách yêu thích ────────────────────────────────────────────────────────────
class YeuThich(Base):
    __tablename__ = "yeu_thich"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    ma_doc_gia   = Column(String(20), ForeignKey("doc_gia.ma_doc_gia"), nullable=False)
    ma_tai_lieu  = Column(String(20), ForeignKey("tai_lieu.ma_tai_lieu"), nullable=False)
    created_at   = Column(DateTime(timezone=True), server_default=func.now())

    doc_gia      = relationship("DocGia")
    tai_lieu     = relationship("TaiLieu")
