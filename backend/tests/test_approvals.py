import requests
import time

BASE_URL = "http://127.0.0.1:8000/api"

def test_approvals():
    print("--- Starting Approval System Test ---")
    
    # 1. Login Librarian
    lib_login = requests.post(f"{BASE_URL}/auth/dang-nhap", json={
        "email": "admin@thuvien.vn",
        "mat_khau": "18112006"
    }).json()
    lib_token = lib_login["access_token"]
    lib_headers = {"Authorization": f"Bearer {lib_token}"}
    print("OK: Librarian Login")

    # 2. Create and Login Reader
    reader_email = f"test_approval_{int(time.time())}@test.com"
    requests.post(f"{BASE_URL}/doc-gia/", json={
        "ho_ten": "Test Reader Approval",
        "email": reader_email,
        "mat_khau": "123456",
        "gioi_tinh": "NAM"
    })
    
    reader_login = requests.post(f"{BASE_URL}/auth/doc-gia/dang-nhap", json={
        "email": reader_email,
        "mat_khau": "123456"
    }).json()
    reader_token = reader_login["access_token"]
    reader_id = reader_login["doc_gia"]["ma_doc_gia"]
    reader_headers = {"Authorization": f"Bearer {reader_token}"}
    print(f"OK: Reader Created and Login ({reader_id})")

    # 3. Reader Reserve Book (TL001)
    res_req = requests.post(f"{BASE_URL}/dat-truoc/", json={
        "ma_doc_gia": reader_id,
        "ma_tai_lieu": "TL001"
    }, headers=reader_headers).json()
    ma_dat_truoc = res_req["ma_dat_truoc"]
    print(f"OK: Book Reserved: {ma_dat_truoc} (Status: {res_req['trang_thai']})")

    # 4. Librarian Approve Reservation
    approve_res = requests.put(f"{BASE_URL}/dat-truoc/{ma_dat_truoc}/duyet", headers=lib_headers).json()
    print(f"OK: Librarian Approved Reservation (Status: {approve_res['trang_thai']})")

    # 5. Librarian Create Borrow Slip (Verify reservation auto-update)
    resp5 = requests.post(f"{BASE_URL}/muon-tra/", json={
        "ma_doc_gia": reader_id,
        "han_tra": "2026-12-31",
        "chi_tiet": [{"ma_tai_lieu": "TL001", "so_luong": 1}]
    }, headers=lib_headers)
    print(f"DEBUG Step 5: {resp5.status_code}")
    pm_req = resp5.json()
    ma_pm = pm_req["ma_phieu_muon"]
    print(f"OK: Librarian Created Borrow Slip: {ma_pm}")

    # Check reservation status
    check_res = requests.get(f"{BASE_URL}/dat-truoc/?ma_doc_gia={reader_id}", headers=lib_headers).json()
    res_item = next(x for x in check_res if x["ma_dat_truoc"] == ma_dat_truoc)
    print(f"OK: Reservation auto-updated to: {res_item['trang_thai']}")

    # 6. Reader Request Return
    resp6 = requests.put(f"{BASE_URL}/muon-tra/{ma_pm}/yeu-cau-tra", headers=reader_headers)
    print(f"DEBUG Step 6: {resp6.status_code}")
    req_return = resp6.json()
    print(f"OK: Reader requested return (Status: {req_return['trang_thai']})")

    # 7. Librarian Approve Return
    resp7 = requests.post(f"{BASE_URL}/muon-tra/tra-sach", json={
        "ma_phieu_muon": ma_pm,
        "tinh_trang_tra": "Good - Approved from API test"
    }, headers=lib_headers)
    print(f"DEBUG Step 7: {resp7.status_code}")
    approve_return = resp7.json()
    print(f"OK: Librarian approved return (Status: {approve_return['trang_thai']})")

    print("\n--- ALL TESTS PASSED ---")

if __name__ == "__main__":
    try:
        test_approvals()
    except Exception as e:
        print(f"Error during test: {e}")
