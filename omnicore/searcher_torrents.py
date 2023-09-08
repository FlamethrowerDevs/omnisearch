import urllib
import requests
from py1337x import py1337x

print("[searcher_torrents] Testing if torrent trackers are reachable...")
try:
    r = requests.get("https://apibay.org/", headers={"User-Agent": "Omnicore-torrents/0.1"})
    if r.status_code in range(200, 300) or r.status_code == 403:
        print("[searcher_torrents] All good for TPB!")
        offline = False
    else:
        print("[searcher_torrents] apibay.org is not reachable! Operation disabled.")
        offline = True
    if not offline:
        r = requests.get("https://1337x.to/", headers={"User-Agent": "Omnicore-torrents/0.1"})
        if r.status_code in range(200, 300):
            print("[searcher_torrents] All good for 1337x!")
            offline = False
        else:
            print("[searcher_torrents] 1337x.to is not reachable! Operation disabled.")
            offline = True
except:
    print("[searcher_torrents] Something didn't work. Operation disabled.")
    offline = True

leetx = py1337x()

# tpb magnet assembly implementation from https://raw.githubusercontent.com/LightDestory/qBittorrent-Search-Plugins/master/src/engines/thepiratebay.py

def assemble_magnet(infohash, name):
    return 'magnet:?xt=urn:btih:{0}&dn={1}&tr=udp%3A%2F%2Ftracker.coppersurfer.tk%3A6969%2Fannounce&tr=udp%3A%2F%2Ftracker.openbittorrent.com%3A6969%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2710%2Fannounce&tr=udp%3A%2F%2F9.rarbg.me%3A2780%2Fannounce&tr=udp%3A%2F%2F9.rarbg.to%3A2730%2Fannounce&tr=udp%3A%2F%2Ftracker.opentrackr.org%3A1337&tr=http%3A%2F%2Fp4p.arenabg.com%3A1337%2Fannounce&tr=udp%3A%2F%2Ftracker.torrent.eu.org%3A451%2Fannounce&tr=udp%3A%2F%2Ftracker.tiny-vps.com%3A6969%2Fannounce&tr=udp%3A%2F%2Fopen.stealth.si%3A80%2Fannounce'.format(infohash, urllib.parse.quote(name))

def search_tpb(query):
    url = f"https://apibay.org/q.php?q={query}&cat=0"
    r = requests.get(url, headers={"User-Agent": "Omnicore-torrents/0.1"})
    magnets = []
    for torrent in r.json():
        magnets.append(assemble_magnet(torrent["info_hash"], torrent["name"]))
    return magnets

def search_leet(query):
    # because 1337x doesn't display magnet links on the search result page, we can't send magnet links directly
    # otherwise, search would be slower and we don't want that
    results = leetx.search(query)
    final = []
    for result in results["items"]:
        final.append(result["link"])
    return final

def search_func(query, config):
    final = []
    if not offline:
        print("[searcher_torrents] Searching TPB...")
        final += search_tpb(query)
        print("[searcher_torrents] Searching 1337x...")
        final += search_leet(query)
    return final
