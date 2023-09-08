import urllib
import requests
from bs4 import BeautifulSoup

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
    print("Took " + str(j["took"]) + "ms")
    if j["timed_out"]:
        print("Timed out!")
        return
    print("Found " + str(len(j["hits"]["hits"])) + " results")
    results = []
    total = len(j["hits"]["hits"])
    for i in j["hits"]["hits"]:
        results.append(i["_source"]["url"])
    return results

def search_func(query, config):
    final = []
    try:
        final += filepursuit(query, FilePursuitType.ALL)
        final += odcrawler(query)
    except:
        pass
    return final
