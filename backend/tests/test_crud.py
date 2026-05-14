import urllib.request, json, datetime

from database import SessionLocal
from models import (
    ChiTietPhieuMuon,
    DatTruoc,
    DocGia,
    PhieuMuon,
    TaiLieu,
    TheThuvien,
    ViPhamPhat,
)

base = 'http://localhost:8000'
TEST_EMAIL = 'testcrud888@test.com'
TEST_TAI_LIEU = 'TLTEST'

def cleanup():
    db = SessionLocal()
    try:
        doc_ids = [
            x[0]
            for x in db.query(DocGia.ma_doc_gia)
            .filter(DocGia.email == TEST_EMAIL)
            .all()
        ]
        pm_ids = [
            x[0]
            for x in db.query(PhieuMuon.ma_phieu_muon)
            .filter(PhieuMuon.ma_doc_gia.in_(doc_ids))
            .all()
        ] if doc_ids else []
        if pm_ids:
            db.query(ViPhamPhat).filter(ViPhamPhat.ma_phieu_muon.in_(pm_ids)).delete(synchronize_session=False)
            db.query(ChiTietPhieuMuon).filter(ChiTietPhieuMuon.ma_phieu_muon.in_(pm_ids)).delete(synchronize_session=False)
            db.query(PhieuMuon).filter(PhieuMuon.ma_phieu_muon.in_(pm_ids)).delete(synchronize_session=False)
        if doc_ids:
            db.query(DatTruoc).filter(DatTruoc.ma_doc_gia.in_(doc_ids)).delete(synchronize_session=False)
            db.query(TheThuvien).filter(TheThuvien.ma_doc_gia.in_(doc_ids)).delete(synchronize_session=False)
            db.query(DocGia).filter(DocGia.ma_doc_gia.in_(doc_ids)).delete(synchronize_session=False)
        db.query(ChiTietPhieuMuon).filter(ChiTietPhieuMuon.ma_tai_lieu == TEST_TAI_LIEU).delete(synchronize_session=False)
        db.query(DatTruoc).filter(DatTruoc.ma_tai_lieu == TEST_TAI_LIEU).delete(synchronize_session=False)
        db.query(TaiLieu).filter(TaiLieu.ma_tai_lieu == TEST_TAI_LIEU).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()

cleanup()

# Login
data = json.dumps({'email':'admin@thuvien.vn','mat_khau':'18112006'}).encode()
req = urllib.request.Request(base+'/api/auth/dang-nhap', data=data, headers={'Content-Type':'application/json'}, method='POST')
r = json.loads(urllib.request.urlopen(req).read())
token = r['access_token']
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def call(method, path, body=None):
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(base+path, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(req)
        raw = resp.read()
        return (json.loads(raw) if raw else {}), resp.getcode()
    except urllib.error.HTTPError as e:
        raw = e.read()
        return (json.loads(raw) if raw else {}), e.code

def ok(c, expected=None):
    if expected:
        return "OK" if c == expected else "FAIL"
    return "OK" if c < 400 else "FAIL"

print("=== CRUD TEST ===")

# CREATE tai lieu
r,c = call('POST','/api/tai-lieu/',{
    'ma_tai_lieu':TEST_TAI_LIEU,'ten_tai_lieu':'Test Book CRUD',
    'nam_xuat_ban':2024,'so_luong':5,'vi_tri':'Ke TEST',
    'ma_tac_gia':'TG001','ma_the_loai':'CNTT','ma_nxb':'NXB001'
})
print(f"[{ok(c,201)}] CREATE tai-lieu: HTTP {c} - {r.get('ma_tai_lieu', str(r)[:80])}")

# UPDATE tai lieu
r,c = call('PUT','/api/tai-lieu/TLTEST',{
    'ten_tai_lieu':'Test Book CRUD Updated','nam_xuat_ban':2024,
    'so_luong':10,'vi_tri':'Ke TEST2',
    'ma_tac_gia':'TG001','ma_the_loai':'CNTT','ma_nxb':'NXB001'
})
print(f"[{ok(c,200)}] UPDATE tai-lieu: HTTP {c} - so_luong={r.get('so_luong','?')}")

# CREATE doc gia
r,c = call('POST','/api/doc-gia/',{
    'ho_ten':'TestDocGia CRUD','ngay_sinh':'2000-01-01',
    'gioi_tinh':'NAM','so_dien_thoai':'0911111888',
    'email':TEST_EMAIL
})
print(f"[{ok(c,201)}] CREATE doc-gia: HTTP {c} - {r.get('ma_doc_gia','?')} {r.get('ho_ten','')}")
ma_dg = r.get('ma_doc_gia')

# CREATE phieu muon
han = (datetime.date.today() + datetime.timedelta(days=14)).isoformat()
r,c = call('POST','/api/muon-tra/',{
    'ma_doc_gia':ma_dg,'han_tra':han,
    'chi_tiet':[{'ma_tai_lieu':TEST_TAI_LIEU,'so_luong':1}]
})
print(f"[{ok(c,201)}] CREATE muon-tra: HTTP {c} - {r.get('ma_phieu_muon', str(r)[:80])}")
ma_pm = r.get('ma_phieu_muon')

# TRA SACH
if ma_pm:
    r,c = call('POST','/api/muon-tra/tra-sach',{'ma_phieu_muon':ma_pm,'tinh_trang_tra':'Tot'})
    print(f"[{ok(c,200)}] TRA SACH: HTTP {c} - trang_thai={r.get('trang_thai','?')}")

# CREATE dat truoc
r,c = call('POST','/api/dat-truoc/',{'ma_doc_gia':'DG000002','ma_tai_lieu':'TL003'})
print(f"[{ok(c,201)}] CREATE dat-truoc: HTTP {c} - {r.get('ma_dat_truoc', str(r)[:80])}")
ma_dt = r.get('ma_dat_truoc')

# HUY dat truoc
if ma_dt:
    r,c = call('PUT',f'/api/dat-truoc/{ma_dt}/huy')
    print(f"[{ok(c,204)}] HUY dat-truoc: HTTP {c}")

# THONG KE
r,c = call('GET','/api/thong-ke/tong-quan')
print(f"[{ok(c,200)}] THONG KE tong-quan: HTTP {c} - {list(r.keys()) if isinstance(r,dict) else r}")

cleanup()
print("=== ALL DONE ===")
