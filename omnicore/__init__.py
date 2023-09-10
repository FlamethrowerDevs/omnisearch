import json
from . import modules

moduleobject = modules.modules

def add_weighted_results(results, weights):
    sorted_results = results
    sorted_results.sort(key=lambda x: sum(weights[i] * x[1] for i, x in enumerate(sorted_results)), reverse=True)
    sorted_items = [item[0] for item in sorted_results]
    return sorted_items

def dosearch(query, config):
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
    for searcher in user_searchers:
        result = searcher["func"](query, config)
        for url in result:
            results.append(url)
    filtered_results = results
    for _filter in user_filters:
        filtered_results = _filter["func"](filtered_results, config)
    for sorter in user_sorters:
        filtered_results = sorter["func"](filtered_results, config, query) # todo: multi-layer sorting based on relevance and weightings
    if not config.get("ignore_forced"): # super-duper-secret dev feature
        for forcedfilter in modules.modules["forcedfilters"]:
            filtered_results = forcedfilter["func"](filtered_results)
    print("[omnicore] Search completed with " + str(len(filtered_results)) + " results.")
    return filtered_results