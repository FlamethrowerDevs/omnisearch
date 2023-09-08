from fuzzyset import FuzzySet
import collections

def fuzzy_sort(results, config, query):
    print("[sorter_generic] Sorting results with fuzzmatch...")
    fuzzset = FuzzySet(use_levenshtein=False, rel_sim_cutoff=float('-inf')) # note negative values to get all results, just sorted by relevance
    for result in results:
        fuzzset.add(result)
    final = []
    try:
        for result in fuzzset.get(query):
            final.append(result[1])
    except:
        pass
    # now we verify that all the results made it through - results turned up from libgen will be hashes but we still want to keep them
    if not collections.Counter(final) == collections.Counter(results):
        print("[sorter_generic] Found missing results, fixing...")
        missing = list(set(results) - set(final))
        final += missing
    return final
