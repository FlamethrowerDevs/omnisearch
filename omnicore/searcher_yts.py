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
    url = f"https://yts.mx/api/v2/list_movies.json?query_term={urllib.parse.quote(query)}&limit=50&"
    r = requests.get(url, headers={"User-Agent": "Omnicore-YTS/0.1"})
    json = r.json()
    try:
        if json["status"] == "ok":
            print("[searcher_yts] Got search response!")
            data = json["data"]["movies"]
            final = []
            for movie in data:
                final.append(movie["url"])
            return final
    except:
        return []
    print("[searcher_yts] Something went wrong.")
    return []