# probably the simplest of the searchers
import libgen_api

def search_func(query, config):
    final = []
    print("[searcher_libgen] Querying libgen...")
    s = libgen_api.LibgenSearch()
    res = s.search_title(query)
    res += s.search_author(query)
    for result in res:
        try:
            final.append(result["Mirror_1"])
            final.append(result["Mirror_2"])
            final.append(result["Mirror_3"])
            final.append(result["Mirror_4"])
            final.append(result["Mirror_5"])
        except:
            pass
    return final

print("[searcher_libgen] Alive!")