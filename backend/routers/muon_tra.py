from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import date, timedelta
from database import get_db
from models import PhieuMuon, ChiTietPhieuMuon, TaiLieu, DocGia, NhanVien, ViPhamPhat, DatTruoc, CauHinhHeThong, TrangThaiPhieu, TrangThaiTaiLieu, TrangThaiThe
from schemas import PhieuMuonCreate, PhieuMuonOut, TraSachRequest
import uuid
import unicodedata

router = APIRouter()

# -------------------- Helper functions --------------------
def gen_ma():
    return "PM-" + date.today().strftime("%Y%m%d") + "-" + uuid.uuid4().hex[:4].upper()

def load_phieu(db, ma):
    pm = db.query(PhieuMuon).options(
        joinedload(PhieuMuon.doc_gia).joinedload(DocGia.the_thu_vien),
        joinedload(PhieuMuon.chi_tiet).joinedload(ChiTietPhieuMuon.tai_lieu),
    ).filter(PhieuMuon.ma_phieu_muon == ma).first()
    # Đảm bảo tất cả chi_tiet.ma_tai_lieu là string (không null)
    if pm:
        for ct in pm.chi_tiet:
            if not ct.ma_tai_lieu:
                ct.ma_tai_lieu = ""
    return pm

def normalize_text(value: str) -> str:
    value = unicodedata.normalize("NFD", value or "")
    value = "".join(ch for ch in value if unicodedata.category(ch) != "Mn")
    return value.lower()

def return_condition_type(tinh_trang_tra: str) -> Optional[str]:
    value = normalize_text(tinh_trang_tra)
    if "mat" in value or "m?t" in value:
        return "lost"
    if "hong" in value or "h?ng" in value or "rach" in value or "r?ch" in value:
        return "damaged"
    return None

def get_int_config(db: Session, key: str, default: int) -> int:
    row = db.query(CauHinhHeThong).filter(CauHinhHeThong.khoa == key).first()
    try:
        return int(row.gia_tri) if row else default
    except ValueError:
        return default

# -------------------- Routes --------------------
@router.get("/qua-han", response_model=List[PhieuMuonOut])
def phieu_qua_han(db: Session = Depends(get_db)):
    today = date.today()
    ds = db.query(PhieuMuon).options(
        joinedload(PhieuMuon.doc_gia).joinedload(DocGia.the_thu_vien),
        joinedload(PhieuMuon.chi_tiet).joinedload(ChiTietPhieuMuon.tai_lieu),
    ).filter(
        PhieuMuon.trang_thai == TrangThaiPhieu.DANG_MUON,
        PhieuMuon.han_tra < today
    ).all()
    for pm in ds:
        pm.trang_thai = TrangThaiPhieu.QUA_HAN
    if ds:
        db.commit()
    return ds

@router.get("/", response_model=List[PhieuMuonOut])
def danh_sach(
    trang_thai: Optional[TrangThaiPhieu] = None,
    ma_doc_gia: Optional[str] = None,
    skip: int = 0, limit: int = 50,
    db: Session = Depends(get_db)
):
    q = db.query(PhieuMuon).options(
        joinedload(PhieuMuon.doc_gia).joinedload(DocGia.the_thu_vien),
        joinedload(PhieuMuon.chi_tiet).joinedload(ChiTietPhieuMuon.tai_lieu),
    )
    if trang_thai:
        q = q.filter(PhieuMuon.trang_thai == trang_thai)
    if ma_doc_gia:
        q = q.filter(PhieuMuon.ma_doc_gia == ma_doc_gia)
    res = q.order_by(PhieuMuon.created_at.desc()).offset(skip).limit(limit).all()
    # Fix chi_tiet.ma_tai_lieu null
    for pm in res:
        for ct in pm.chi_tiet:
            if not ct.ma_tai_lieu:
                ct.ma_tai_lieu = ""
    return res

@router.get("/lich-su/{ma_doc_gia}", response_model=List[PhieuMuonOut])
def lich_su_doc_gia(ma_doc_gia: str, db: Session = Depends(get_db)):
    res = db.query(PhieuMuon).options(
        joinedload(PhieuMuon.doc_gia).joinedload(DocGia.the_thu_vien),
        joinedload(PhieuMuon.chi_tiet).joinedload(ChiTietPhieuMuon.tai_lieu),
    ).filter(PhieuMuon.ma_doc_gia == ma_doc_gia).order_by(PhieuMuon.created_at.desc()).all()
    for pm in res:
        for ct in pm.chi_tiet:
            if not ct.ma_tai_lieu:
                ct.ma_tai_lieu = ""
    return res

@router.get("/{ma}", response_model=PhieuMuonOut)
def chi_tiet(ma: str, db: Session = Depends(get_db)):
    pm = load_phieu(db, ma)
    if not pm:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    return pm

@router.get("/dat-truoc/{ma}", response_model=dict)
def get_reservation_info(ma: str, db: Session = Depends(get_db)):
    dt = db.query(DatTruoc).options(
        joinedload(DatTruoc.doc_gia),
        joinedload(DatTruoc.tai_lieu)
    ).filter(DatTruoc.ma_dat_truoc == ma).first()
    if not dt:
        raise HTTPException(404, "Không tìm thấy mã đặt trước")
    
    # Kiểm tra trạng thái - chỉ cho phép nếu chưa nhận sách
    if dt.trang_thai == "da_nhan_sach":
         raise HTTPException(400, "Mã đặt trước này đã được nhận sách rồi")

    return {
        "ma_doc_gia": dt.ma_doc_gia,
        "ho_ten": dt.doc_gia.ho_ten if dt.doc_gia else "N/A",
        "ma_tai_lieu": dt.ma_tai_lieu,
        "ten_tai_lieu": dt.tai_lieu.ten_tai_lieu if dt.tai_lieu else "N/A",
        "so_luong": 1,
        "ma_dat_truoc": dt.ma_dat_truoc
    }

@router.put("/{ma}/gia-han", response_model=PhieuMuonOut)
def gia_han(ma: str, db: Session = Depends(get_db)):
    pm = load_phieu(db, ma)
    if not pm:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    if pm.trang_thai not in (TrangThaiPhieu.DANG_MUON, TrangThaiPhieu.QUA_HAN):
        raise HTTPException(400, "Chỉ gia hạn phiếu đang mượn hoặc quá hạn")
    for ct in pm.chi_tiet:
        exists = db.query(DatTruoc).filter(
            DatTruoc.ma_tai_lieu == ct.ma_tai_lieu,
            DatTruoc.trang_thai == "cho_xu_ly"
        ).first()
        if exists:
            raise HTTPException(400, f"Tài liệu {ct.ma_tai_lieu} đang có đặt trước, không thể gia hạn")
    days = get_int_config(db, "so_ngay_gia_han", 7)
    pm.han_tra = pm.han_tra + timedelta(days=days)
    if pm.han_tra >= date.today():
        pm.trang_thai = TrangThaiPhieu.DANG_MUON
    db.commit()
    return load_phieu(db, ma)

@router.post("/", response_model=PhieuMuonOut, status_code=201)
def lap_phieu_muon(req: PhieuMuonCreate, db: Session = Depends(get_db)):
    dg = db.query(DocGia).filter(DocGia.ma_doc_gia == req.ma_doc_gia).first()
    if not dg:
        raise HTTPException(400, "Không tìm thấy độc giả")
    if dg.trang_thai_the != TrangThaiThe.CON_HIEU_LUC:
        raise HTTPException(400, "Thẻ độc giả không còn hiệu lực")

    dang_muon = db.query(PhieuMuon).filter(
        PhieuMuon.ma_doc_gia == req.ma_doc_gia,
        PhieuMuon.trang_thai == TrangThaiPhieu.DANG_MUON
    ).count()
    max_books = get_int_config(db, "so_sach_toi_da", 5)
    if dang_muon >= max_books:
        raise HTTPException(400, f"Độc giả đã mượn tối đa {max_books} cuốn")

    nv = db.query(NhanVien).first()
    ma_nv = nv.ma_nhan_vien if nv else None

    ma = gen_ma()
    pm = PhieuMuon(
        ma_phieu_muon=ma,
        ngay_muon=date.today(),
        han_tra=req.han_tra,
        ghi_chu=req.ghi_chu,
        ma_doc_gia=req.ma_doc_gia,
        ma_nhan_vien=ma_nv,
    )
    db.add(pm)

    for ct in req.chi_tiet:
        tl = db.query(TaiLieu).filter(TaiLieu.ma_tai_lieu == ct.ma_tai_lieu).first()
        if not tl:
            db.rollback()
            raise HTTPException(400, f"Tài liệu {ct.ma_tai_lieu} không tồn tại")
        if tl.so_luong < ct.so_luong:
            db.rollback()
            raise HTTPException(400, f"Tài liệu '{tl.ten_tai_lieu}' không đủ số lượng (còn {tl.so_luong})")
        tl.so_luong -= ct.so_luong
        if tl.so_luong == 0:
            tl.tinh_trang = TrangThaiTaiLieu.DANG_MUON
        db.add(ChiTietPhieuMuon(
            ma_phieu_muon=ma,
            ma_tai_lieu=ct.ma_tai_lieu or "",  # đảm bảo không null
            so_luong=ct.so_luong,
        ))

        # Tự động hoàn tất đặt trước khi đã tạo phiếu mượn
        db.query(DatTruoc).filter(
            DatTruoc.ma_doc_gia == req.ma_doc_gia,
            DatTruoc.ma_tai_lieu == ct.ma_tai_lieu,
            DatTruoc.trang_thai.in_(["cho_xu_ly", "da_duyet"])
        ).update({"trang_thai": "da_nhan_sach"}, synchronize_session="fetch")

    db.commit()
    return load_phieu(db, ma)

@router.put("/{ma}/yeu-cau-tra", response_model=PhieuMuonOut)
def yeu_cau_tra(ma: str, db: Session = Depends(get_db)):
    """Độc giả yêu cầu trả sách — chờ thủ thư duyệt."""
    pm = load_phieu(db, ma)
    if not pm:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    if pm.trang_thai not in (TrangThaiPhieu.DANG_MUON, TrangThaiPhieu.QUA_HAN):
        raise HTTPException(400, "Chỉ có thể yêu cầu trả phiếu đang mượn")
    pm.trang_thai = TrangThaiPhieu.CHO_TRA
    db.commit()
    return load_phieu(db, ma)

@router.post("/tra-sach", response_model=PhieuMuonOut)
def tra_sach(req: TraSachRequest, db: Session = Depends(get_db)):
    pm = db.query(PhieuMuon).options(
        joinedload(PhieuMuon.chi_tiet).joinedload(ChiTietPhieuMuon.tai_lieu)
    ).filter(PhieuMuon.ma_phieu_muon == req.ma_phieu_muon).first()
    if not pm:
        raise HTTPException(404, "Không tìm thấy phiếu mượn")
    if pm.trang_thai == TrangThaiPhieu.DA_TRA:
        raise HTTPException(400, "Phiếu này đã được trả rồi")

    pm.trang_thai = TrangThaiPhieu.DA_TRA
    condition_type = return_condition_type(req.tinh_trang_tra)
    total_fine = 0
    for ct in pm.chi_tiet:
        tl = ct.tai_lieu or db.query(TaiLieu).filter(TaiLieu.ma_tai_lieu == ct.ma_tai_lieu).first()
        if tl:
            if condition_type:
                total_fine += int(tl.gia or 0) * int(ct.so_luong or 1)
                if tl.so_luong == 0:
                    tl.tinh_trang = TrangThaiTaiLieu.BAO_TRI if condition_type == "damaged" else TrangThaiTaiLieu.THANH_LY
            else:
                tl.so_luong += ct.so_luong
                tl.tinh_trang = TrangThaiTaiLieu.CO_SAN
        ct.ngay_tra = date.today()
        ct.tinh_trang_tra = req.tinh_trang_tra
        # Fix ma_tai_lieu null
        if not ct.ma_tai_lieu:
            ct.ma_tai_lieu = ""

    if condition_type and total_fine <= 0:
        raise HTTPException(400, "Chưa có giá sách để tính phạt mất/hỏng")

    if condition_type:
        label = "Mất sách" if condition_type == "lost" else "Sách rách/hỏng"
        db.add(ViPhamPhat(
            ma_phat="VP-" + uuid.uuid4().hex[:8].upper(),
            ly_do_phat=f"{label} - tính theo giá sách",
            so_tien=total_fine,
            ma_phieu_muon=pm.ma_phieu_muon,
        ))

    db.commit()
    return load_phieu(db, req.ma_phieu_muon)