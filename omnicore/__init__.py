import json
from . import modules

moduleobject = modules.modules

def dosearch(query, config):
    print("search for:", query, "and conf", config)
    try:
        config = json.loads(config)
    except:
        config = {"sorters": ["Fuzzy Match"], "filters": [], "searchers": ["Torrent Trackers", "The Eyedex", "Local Archive", "YTS/YIFY", "Game Repackers", "Opendirectory Indexes", "Library Genesis"]} # default config for when i break things
    user_searchers = []
    user_filters   = []
    user_sorters   = []
    print("Finding active modules...")
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
    if not config.get("ignore_forced"):
        for forcedfilter in modules.modules["forcedfilters"]:
            filtered_results = forcedfilter["func"](filtered_results)
    return filtered_results