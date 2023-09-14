import json
from urllib.parse import unquote
import requests
from . import modules

moduleobject = modules.modules

def add_weighted_results(results, weights):
    sorted_results = results
    sorted_results.sort(key=lambda x: sum(weights[i] * x[1] for i, x in enumerate(sorted_results)), reverse=True)
    sorted_items = [item[0] for item in sorted_results]
    return sorted_items

def dosearch(query, config, return_responsible=False):
    print("[omnicore] Searching for: " + query)
    try:
        config = json.loads(config)
    except:
        config = {"sorters": ["Fuzzy Match"], "filters": [], "searchers": ["Torrent Trackers", "The Eyedex", "Local Archive", "YTS/YIFY", "Game Repackers", "Opendirectory Indexes", "Library Genesis"]} # default config
    user_searchers = []
    user_filters   = []
    user_sorters   = []
    print("[omnicore] Finding active modules...")
    for searcher in config["searchers"]:
        for _searcher in modules.modules["searchers"]:
            if searcher == _searcher["name"] or searcher == _searcher["id"]:
                user_searchers.append(_searcher)
    for _filter in config["filters"]:
        for __filter in modules.modules["filters"]:
            if _filter == __filter["name"] or _filter == __filter["id"]:
                user_filters.append(__filter)
    for sorter in config["sorters"]:
        for _sorter in modules.modules["sorters"]:
            if sorter == _sorter["name"] or sorter == _sorter["id"]:
                user_sorters.append(_sorter)
    results = []
    responsible_searchers = []
    for searcher in user_searchers:
        result = searcher["func"](query, config)
        for url in result:
            results.append(url)
            responsible_searchers.append(searcher["name"])
    filtered_results = results
    for _filter in user_filters:
        filtered_results = _filter["func"](filtered_results, config)
    for sorter in user_sorters:
        filtered_results = sorter["func"](filtered_results, config, query) # todo: multi-layer sorting based on relevance and weightings
    if not config.get("ignore_forced"): # super-duper-secret dev feature
        for forcedfilter in modules.modules["forcedfilters"]:
            filtered_results = forcedfilter["func"](filtered_results)
    print("[omnicore] Search completed with " + str(len(filtered_results)) + " results.")
    if not return_responsible:
        return filtered_results
    return filtered_results, responsible_searchers

def extract_magnet_title(magnet):
    return unquote(magnet.split("&dn=")[1].split("&")[0])

def fix_weird_format(text):
    return text.replace("\n", " ").replace("\r", " ").replace("\t", " ").replace("<br>", " ").strip()

def combined_extract(url):
    r = requests.get(url, stream=True, timeout=6) # idk how long to wait - how slow are we expecting results to be anyway?
    title = "Unknown"
    if not r.status_code in range(200, 300):
        title = "Non-valid status code" + str(r.status_code)
    else:
        if "text/html" in r.headers["content-type"]:
            try:
                title = r.text.split("<title>")[1].split("</title>")[0]
            except:
                title = "Unable to extract title from HTML"
        else:
            title = url
    desc = "Unknown"
    if not r.status_code in range(200, 300):
        desc = "Non-valid status code" + str(r.status_code)
    else:
        if "text/html" in r.headers["content-type"]:
            try:
                desc = fix_weird_format(r.text.split("<meta name=\"description\" content=\"")[1].split("\"")[0])
            except:
                # try to get a snippet of text from the page
                try:
                    desc = fix_weird_format(r.text.split("<p>")[1].split("</p>")[0])
                except:
                    desc = "Unable to extract description/snippet from HTML"
        else:
            desc = r.headers["content-type"]
    return title, desc

def evaluate_trust(url):
    trustworthiness = 0.5
    reason = "Unknown"
    if "magnet:?" in url:
        trustworthiness = 0.5
        reason = "Magnet links are not easily verifiable. Many are safe to use, just don't execute any files you download from them unless you're sure of what you're doing."
        print("[omnicore] Magnet link auto-detection broke somehow, please report this bug on GitHub.")
    else:
        for scam in modules.scamdomains:
            if scam["match"] in url:
                trustworthiness -= scam["weight"]
                reason = "Untrustworthy domain"
                break
    return trustworthiness, reason

def enhancedsearch(query, config):
    results, responsible = dosearch(query, config, return_responsible=True)
    print("[omnicore] Enhancing results...")
    enhanced_results = [] # these are in a different format, and the old search function is left intact for backwards compatibility (see below)
    # each entry in the results contains:
    # 0: url
    # 1: responsible searcher
    # 2: page title, if it can be extracted, otherwise the filename (especially for magnets) - TODO: extract titles for libgen results or provide some way for modules to provide custom titles (that would make my life so much easier)
    # 3: meta description, if it can be extracted, otherwise text snippet if file is not binary - if file is binary, content-type header
    # 4: trustworthiness score
    # 5: trustworthiness reason

    for result in results:
        if result.startswith("magnet:?"):
            enhanced_results.append([result, responsible[results.index(result)], extract_magnet_title(result), "Magnet link", 0.5, "Magnet links are not easily verifiable. Many are safe to use, just don't execute any files you download from them unless you're sure of what you're doing."])
        else:
            print("[omnicore] Enhancing " + result + "...")
            trustworthiness, reason = evaluate_trust(result) # evaluate_trust is done offline, it just checks for scam domains and such
            title, desc = combined_extract(result)
            enhanced_results.append([result, responsible[results.index(result)], title, desc, trustworthiness, reason])