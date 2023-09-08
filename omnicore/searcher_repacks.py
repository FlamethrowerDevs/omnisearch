import requests
from bs4 import BeautifulSoup
import urllib.parse

ignore_dodi = True

print("[searcher_repacks] Testing if FitGirl and DODI are reachable...")
try:
    r = requests.get("https://fitgirl-repacks.site/", headers={"User-Agent": "Omnicore-repacks/0.1"})
    if r.status_code in range(200, 300):
        print("[searcher_repacks] All good for FitGirl!")
        offline = False
    else:
        print("[searcher_repacks] FitGirl is not reachable! Operation disabled.")
        offline = True
    if not ignore_dodi:
        r = requests.get("https://dodi-repacks.site/", headers={"User-Agent": "Omnicore-repacks/0.1"})
        if r.status_code in range(200, 300):
            print("[searcher_repacks] All good for DODI!")
            offline = False
        else:
            print("[searcher_repacks] DODI is not reachable! Operation disabled.")
            print(r.status_code, r.text)
            offline = True
except:
    print("[searcher_repacks] Something didn't work. Operation disabled.")
    offline = True

def continue_link(elem):
    return elem.name=='a' and 'continue reading' in str(elem).lower()

def search_func(query, config):
    if offline:
        return []
    final = []
    urls = [f"https://fitgirl-repacks.site/?s={urllib.parse.quote(query)}", f"https://dodi-repacks.site/?s={urllib.parse.quote(query)}"] if not ignore_dodi else [f"https://fitgirl-repacks.site/?s={urllib.parse.quote(query)}"]
    responses = []
    for url in urls:
        responses.append(requests.get(url, headers={"User-Agent": "Omnicore-repacks/0.1"}))
    for r in responses:
        soup = BeautifulSoup(r.text, "html.parser")
        links = soup.find_all(continue_link)
        for link in links:
            final.append(link["href"])
    return final