from fuzzyset import FuzzySet

def fuzzy_sort(results, config, query):
    fuzzset = FuzzySet(use_levenshtein=False, rel_sim_cutoff=0.0) # note 0.0 to get all results, just sorted by relevance
    for result in results:
        fuzzset.add(result)
    final = []
    for result in fuzzset.get(query):
        final.append(result[1])
    return final
