import urllib
import requests
from bs4 import BeautifulSoup

print("[searcher_odindexers] Testing if OD indexers are reachable...")
try:
    r = requests.get("https://filepursuit.com/", headers={"User-Agent": "Omnicore-odindexers/0.1"})
    if r.status_code in range(200, 300):
        print("[searcher_odindexers] All good!")
        offline = False
    else:
        print("[searcher_odindexers] Filepursuit is not reachable! Operation disabled.")
        offline = True
except:
    print("[searcher_odindexers] Something didn't work. Operation disabled.")
    offline = True

class FilePursuitType:
    VIDEO = "video"
    AUDIO = "audio"
    BOOKS = "ebook"
    APPS = "mobile"
    ARCHIVES = "archive"
    ALL = "all"

def filepursuit(searchterm, ftype, limit=None):
    encoded = urllib.parse.quote(searchterm).replace("%20", "+")
    url = "https://filepursuit.com/pursuit?q=" + encoded + "&type=" + ftype + "&sort=datedesc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a")
    # now we sift through and find only the ones that are actually files - they start with "/discover.php?link="
    files = []
    for link in links:
        try:
            if link.get("href").startswith("/discover.php?link="):
                files.append(link.get("href"))
        except:
            # shut up, python
            pass
    files2 = []
    for file in files:
        if file[19:] not in files2:
            files2.append(file[19:])
    return files2

def odcrawler(query, limit=10):
    payload = {"size":limit,"from":0,"highlight":{"fields":{"url":{},"filename":{}}},"query":{"bool":{"must":[{"match_phrase":{"url":query}}],"should":[{"match_phrase":{"filename":query}}],"must_not":[{"terms":{"extension":["html","html","HTML"]}}]}}}
    target = "https://search.odcrawler.xyz/elastic/links/_search"
    r = requests.post(target, json=payload)
    j = r.json()
    if j["timed_out"]:
        print("[searcher_odindexers] Timed out!")
        return
    results = []
    total = len(j["hits"]["hits"])
    for i in j["hits"]["hits"]:
        results.append(i["_source"]["url"])
    return results

def search_func(query, config):
    if offline:
        return []
    final = []
    try:
        final += filepursuit(query, FilePursuitType.ALL)
        final += odcrawler(query)
    except:
        pass
    actual_final = []
    for url in final:
        actual_final.append(url.replace("%20", " "))
    print("[searcher_odindexers] Found", len(final), "results")
    return actual_final
