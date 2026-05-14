import requests
try:
    headers = {
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'authorization'
    }
    r = requests.options('http://127.0.0.1:8000/api/dat-truoc/', headers=headers)
    print(f"Status: {r.status_code}")
    print(f"Headers: {dict(r.headers)}")
except Exception as e:
    print(f"Error: {e}")
