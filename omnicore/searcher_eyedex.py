import requests
from bs4 import BeautifulSoup
import urllib.parse

pagecount = 3 # 3-5 pages of results works best

print("[searcher_eyedex] Testing if the Eyedex is reachable...")
try:
    r = requests.get("https://www.eyedex.org/", headers={"User-Agent": "Omnicore-Eyedex/0.1"})
    if r.status_code in range(200, 300):
        print("[searcher_eyedex] All good!")
        offline = False
    else:
        print("[searcher_eyedex] The Eyedex is not reachable! Operation disabled.")
        offline = True
except:
    print("[searcher_eyedex] Something didn't work. Operation disabled.")
    offline = True

def search_page(query, pagenum):
    encoded_query = urllib.parse.quote(query)
    encoded_query = encoded_query.replace("%20", "+")
    url = f"https://www.eyedex.org/search/?q={encoded_query}&p={str(pagenum)}"
    print("[searcher_eyedex] Making request to", url)
    r = requests.get(url, headers={"User-Agent": "Omnicore-Eyedex/0.1"})
    soup = BeautifulSoup(r.text, "html.parser")
    results = []
    for result in soup.find_all(name="tr")[1:]:
        url = result.find_all("td")[2].find("nobr").find("a").get("href")
        results.append(urllib.parse.unquote(url)) # decode for better fuzzy match later
    return results

def search_func(query, config):
    if offline:
        return []
    print("[searcher_eyedex] Searching for", query, "with pagecount", pagecount)
    results = []
    for i in range(0, pagecount):
        results += search_page(query, i)
    print("[searcher_eyedex] Found", len(results), "results from Eyedex.")
    return results
