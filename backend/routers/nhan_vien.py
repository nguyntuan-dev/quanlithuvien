from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import NhanVien
from routers.auth import require_admin
from schemas import NhanVienCreate, NhanVienOut
import hashlib, uuid

router = APIRouter()

@router.get("/", response_model=List[NhanVienOut])
def danh_sach(
    db: Session = Depends(get_db),
    current: NhanVien = Depends(require_admin),
):
    return db.query(NhanVien).all()

@router.get("/{ma}", response_model=NhanVienOut)
def chi_tiet(
    ma: str,
    db: Session = Depends(get_db),
    current: NhanVien = Depends(require_admin),
):
    nv = db.query(NhanVien).filter(NhanVien.ma_nhan_vien == ma).first()
    if not nv:
        raise HTTPException(404, "Không tìm thấy nhân viên")
    return nv

@router.post("/", response_model=NhanVienOut, status_code=201)
def them_moi(
    req: NhanVienCreate,
    db: Session = Depends(get_db),
    current: NhanVien = Depends(require_admin),
):
    if db.query(NhanVien).filter(NhanVien.email == req.email).first():
        raise HTTPException(400, "Email đã tồn tại")
    ma = "NV" + uuid.uuid4().hex[:6].upper()
    nv = NhanVien(
        ma_nhan_vien=ma,
        ho_ten=req.ho_ten,
        chuc_vu=req.chuc_vu,
        so_dien_thoai=req.so_dien_thoai,
        email=req.email,
        mat_khau_hash=hashlib.sha256(req.mat_khau.encode()).hexdigest(),
        la_admin=req.la_admin,
    )
    db.add(nv); db.commit(); db.refresh(nv)
    return nv

@router.delete("/{ma}", status_code=204)
def xoa(
    ma: str,
    db: Session = Depends(get_db),
    current: NhanVien = Depends(require_admin),
):
    nv = db.query(NhanVien).filter(NhanVien.ma_nhan_vien == ma).first()
    if not nv:
        raise HTTPException(404, "Không tìm thấy nhân viên")
    db.delete(nv); db.commit()
