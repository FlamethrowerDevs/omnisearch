import os
try:
    from cfuzzyset import cFuzzySet as FuzzySet
except ImportError:
    from fuzzyset import FuzzySet

print("Loading archive contents...")
fuzzset = fuzzyset.FuzzySet()
searchpath = "./archives"
if not os.path.exists(searchpath):
    os.makedirs(searchpath)
finalstr = ""
for file in os.listdir(searchpath):
    print("Loading " + file + "...")
    with open(os.path.join("./archives", file), "r") as f:
        finalstr += f.read() + "\n"
        f.close()
print("Adding strings to fuzzy set...")
fuzzset.add(finalstr)

def search_func(query, config):
    results = fuzzset.get(query)
    final = []
    for result in results:
        final.append(str(result[1]))