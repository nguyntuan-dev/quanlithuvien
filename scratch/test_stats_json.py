import requests
import json

def test():
    urls = [
        'http://127.0.0.1:8000/api/thong-ke/tong-quan',
        'http://127.0.0.1:8000/api/thong-ke/muon-theo-thang',
        'http://127.0.0.1:8000/api/thong-ke/top-tai-lieu'
    ]
    results = {}
    for url in urls:
        try:
            r = requests.get(url)
            results[url] = {
                "status": r.status_code,
                "body": r.json() if r.status_code == 200 else r.text
            }
        except Exception as e:
            results[url] = {"error": str(e)}
    
    with open('e:/quanlithuvien1/scratch/stats_debug.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    test()
