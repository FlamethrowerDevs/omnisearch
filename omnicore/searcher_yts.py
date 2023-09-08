import requests
import urllib.parse

print("[searcher_yts] Testing if YTS is reachable...")
try:
    r = requests.get("https://yts.mx/", headers={"User-Agent": "Omnicore-YTS/0.1"})
    if r.status_code in range(200, 300):
        print("[searcher_yts] All good!")
        offline = False
    else:
        print("[searcher_yts] YTS is not reachable! Operation disabled.")
        offline = True
except:
    print("[searcher_yts] Something didn't work. Operation disabled.")
    offline = True

def search_func(query, config):
    if offline:
        return []
    return []