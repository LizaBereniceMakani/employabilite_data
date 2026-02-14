import requests

ID_OFFRE = "178077294W" # The one with truncated text

URLS = [
    f"https://www.apec.fr/cms/webservices/offre/public/offre/{ID_OFFRE}",
    f"https://www.apec.fr/cms/webservices/rechercheOffre/detail/{ID_OFFRE}",
    f"https://www.apec.fr/cms/webservices/offre/{ID_OFFRE}"
]
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Content-Type": "application/json"
}

for url in URLS:
    try:
        print(f"Testing {url} ...")
        r = requests.get(url, headers=HEADERS, timeout=5)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            # Chercher un champ long
            print("Keys:", data.keys())
            for k, v in data.items():
                if isinstance(v, str) and len(v) > 500:
                    print(f"FOUND LONG FIELD: {k} (Len: {len(v)})")
                    print(v[:200] + "...")
            break
    except Exception as e:
        print(e)
