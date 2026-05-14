import requests
urls = [
    'http://127.0.0.1:8000/api/thong-ke/tong-quan',
    'http://127.0.0.1:8000/api/thong-ke/muon-theo-thang',
    'http://127.0.0.1:8000/api/thong-ke/top-tai-lieu'
]
for url in urls:
    try:
        r = requests.get(url)
        print(f"URL: {url}")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print(f"Body: {r.json()}")
        else:
            print(f"Error Body: {r.text}")
    except Exception as e:
        print(f"URL: {url} - Error: {e}")
    print("-" * 20)
