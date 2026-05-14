"""
Hệ thống tự động hóa cho thư viện
"""
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from database import SessionLocal
from models import (
    PhieuMuon, ViPhamPhat, DocGia, TrangThaiPhieu, TrangThaiThe, TrangThaiPhat,
    DatTruoc, CauHinhHeThong
)
import os
from dotenv import load_dotenv
from utils.email import send_email, LIBRARY_NAME

load_dotenv()

# ── Hệ số phạt ────────────────────────────────────────────────────────────────
FINE_PER_DAY_OVERDUE = 10000     # 10k/ngày quá hạn
LOST_BOOK_COEFFICIENT = 2.0      # Phạt 200% giá sách nếu mất
BROKEN_BOOK_COEFFICIENT = 0.5    # Phạt 50% giá sách nếu hỏng (tùy mức độ)

def get_int_config(db, key: str, default: int) -> int:
    row = db.query(CauHinhHeThong).filter(CauHinhHeThong.khoa == key).first()
    try:
        return int(row.gia_tri) if row else default
    except ValueError:
        return default

def job_update_overdue():
    """[JOB 1] Cập nhật phiếu mượn quá hạn mỗi ngày lúc 00:00"""
    db = SessionLocal()
    try:
        today = date.today()
        overdue_phieu = db.query(PhieuMuon).filter(
            PhieuMuon.trang_thai == TrangThaiPhieu.DANG_MUON,
            PhieuMuon.han_tra < today
        ).all()
        
        for pm in overdue_phieu:
            pm.trang_thai = TrangThaiPhieu.QUA_HAN
        
        db.commit()
        print(f"[OK] Updated {len(overdue_phieu)} phiếu quá hạn")
    except Exception as e:
        print(f"[ERROR] Error in update_overdue: {e}")
        db.rollback()
    finally:
        db.close()

def job_calculate_daily_fine():
    """[JOB 2] Tính phạt tự động cho phiếu quá hạn & Gửi email"""
    db = SessionLocal()
    try:
        today = date.today()
        overdue_phieu = db.query(PhieuMuon).filter(
            PhieuMuon.trang_thai == TrangThaiPhieu.QUA_HAN
        ).all()
        
        for pm in overdue_phieu:
            existing_vp = db.query(ViPhamPhat).filter(
                ViPhamPhat.ma_phieu_muon == pm.ma_phieu_muon,
                ViPhamPhat.ly_do_phat.like("Quá hạn trả sách%")
            ).first()
            
            if not existing_vp:
                so_ngay_qua_han = (today - pm.han_tra).days
                so_tien = so_ngay_qua_han * get_int_config(db, "tien_phat_qua_han_moi_ngay", FINE_PER_DAY_OVERDUE)
                
                vp = ViPhamPhat(
                    ma_phat=f"VP-{pm.ma_phieu_muon}-{today.isoformat()}",
                    ly_do_phat=f"Quá hạn trả sách ({so_ngay_qua_han} ngày)",
                    so_tien=so_tien,
                    ma_phieu_muon=pm.ma_phieu_muon,
                )
                db.add(vp)

                # Gửi email thông báo
                dg = pm.doc_gia
                if dg and dg.email:
                    email_body = f"""
                    <h2>Thông báo vi phạm quá hạn</h2>
                    <p>Kính gửi {dg.ho_ten},</p>
                    <p>Bạn đã quá hạn trả sách <strong>{so_ngay_qua_han} ngày</strong>.</p>
                    <p>Số tiền phạt hiện tại: <strong>{so_tien:,} VNĐ</strong></p>
                    <p>Vui lòng trả sách và thanh toán sớm để tránh bị khóa thẻ.</p>
                    <p>Trân trọng,<br/><strong>{LIBRARY_NAME}</strong></p>
                    """
                    send_email(dg.email, "Thông báo phạt quá hạn sách", email_body)
        
        db.commit()
        print(f"[OK] Calculated daily fines")
    except Exception as e:
        print(f"[ERROR] Error in calculate_daily_fine: {e}")
        db.rollback()
    finally:
        db.close()

def job_send_overdue_notifications():
    """[JOB 3] Gửi email thông báo sách sắp đến hạn (2 ngày trước hạn)"""
    db = SessionLocal()
    try:
        today = date.today()
        remind_date = today + timedelta(days=2)
        phieu_sap_han = db.query(PhieuMuon).filter(
            PhieuMuon.trang_thai == TrangThaiPhieu.DANG_MUON,
            PhieuMuon.han_tra == remind_date
        ).all()
        
        for pm in phieu_sap_han:
            dg = pm.doc_gia
            if dg and dg.email:
                email_body = f"""
                <h2>Thông báo hạn trả sách</h2>
                <p>Kính gửi {dg.ho_ten},</p>
                <p>Sách bạn mượn sắp đến hạn trả vào ngày <strong>{pm.han_tra}</strong></p>
                <p>Vui lòng trả sách đúng hạn để tránh bị phạt.</p>
                <p>Trân trọng,<br/><strong>{LIBRARY_NAME}</strong></p>
                """
                send_email(dg.email, "Thông báo hạn trả sách", email_body)
        print(f"[OK] Sent reminder emails")
    except Exception as e:
        print(f"[ERROR] Error in send_overdue_notifications: {e}")
    finally:
        db.close()

def job_lock_card_on_violation():
    """[JOB 4] Tự động khóa thẻ nếu có vi phạm chưa thanh toán"""
    db = SessionLocal()
    try:
        doc_gia_co_vp = db.query(DocGia).join(PhieuMuon).join(ViPhamPhat).filter(
            ViPhamPhat.trang_thai_thanh_toan == TrangThaiPhat.CHUA_THANH_TOAN
        ).distinct().all()
        
        for dg in doc_gia_co_vp:
            if dg.trang_thai_the != TrangThaiThe.BI_KHOA:
                dg.trang_thai_the = TrangThaiThe.BI_KHOA
                if dg.email:
                    email_body = f"<h2>Thẻ thư viện bị khóa</h2><p>Chào {dg.ho_ten}, thẻ của bạn đã bị khóa do có vi phạm chưa thanh toán.</p>"
                    send_email(dg.email, "Thẻ thư viện bị khóa", email_body)
        db.commit()
    except Exception as e:
        print(f"[ERROR] Error in lock_card: {e}")
    finally:
        db.close()

def job_cancel_old_reservations():
    """[JOB 5] Hủy đặt trước cũ (>7 ngày)"""
    db = SessionLocal()
    try:
        cancel_before = datetime.now() - timedelta(days=7)
        old_res = db.query(DatTruoc).filter(DatTruoc.trang_thai == "cho_xu_ly", DatTruoc.ngay_dat < cancel_before).all()
        for dt in old_res:
            dt.trang_thai = "da_huy"
        db.commit()
    except Exception as e:
        print(f"[ERROR] Error in cancel_reservations: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(job_update_overdue, 'cron', hour=0, minute=0, id='update_overdue')
    scheduler.add_job(job_calculate_daily_fine, 'cron', hour=0, minute=5, id='calculate_fine')
    scheduler.add_job(job_send_overdue_notifications, 'cron', hour=8, minute=0, id='send_notifications')
    scheduler.add_job(job_lock_card_on_violation, 'cron', hour='*/6', minute=0, id='lock_card')
    scheduler.add_job(job_cancel_old_reservations, 'cron', day_of_week='mon', hour=0, minute=0, id='cancel_res')
    scheduler.start()
    print("[OK] Scheduler started with 5 automation jobs")
    return scheduler
