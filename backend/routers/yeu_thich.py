from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from database import get_db
from models import YeuThich, TaiLieu, DocGia
from schemas import YeuThichCreate, YeuThichOut
from routers.auth import get_current_doc_gia

router = APIRouter()

@router.get("/", response_model=List[YeuThichOut])
def danh_sach_yeu_thich(
    db: Session = Depends(get_db),
    dg: DocGia = Depends(get_current_doc_gia)
):
    return db.query(YeuThich).options(
        joinedload(YeuThich.tai_lieu)
    ).filter(YeuThich.ma_doc_gia == dg.ma_doc_gia).all()

@router.post("/", response_model=YeuThichOut, status_code=201)
def them_yeu_thich(
    req: YeuThichCreate,
    db: Session = Depends(get_db),
    dg: DocGia = Depends(get_current_doc_gia)
):
    # Kiểm tra tồn tại
    existing = db.query(YeuThich).filter(
        YeuThich.ma_doc_gia == dg.ma_doc_gia,
        YeuThich.ma_tai_lieu == req.ma_tai_lieu
    ).first()
    if existing:
        return existing
    
    yt = YeuThich(ma_doc_gia=dg.ma_doc_gia, ma_tai_lieu=req.ma_tai_lieu)
    db.add(yt); db.commit(); db.refresh(yt)
    return yt

@router.delete("/{ma_tai_lieu}", status_code=204)
def xoa_yeu_thich(
    ma_tai_lieu: str,
    db: Session = Depends(get_db),
    dg: DocGia = Depends(get_current_doc_gia)
):
    yt = db.query(YeuThich).filter(
        YeuThich.ma_doc_gia == dg.ma_doc_gia,
        YeuThich.ma_tai_lieu == ma_tai_lieu
    ).first()
    
    if yt:
        db.delete(yt); db.commit()
    return None
