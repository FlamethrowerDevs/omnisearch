import os
import requests
from fuzzyset import FuzzySet

print("Pruning archives...")
for file in os.listdir("./archives"):
    if file.endswith(".txt") and not file.startswith("_"):
        dir = os.path.join("./archives", file)
        with open(dir, "r", errors='replace') as f:
            line = f.readline()
            # send a get request and abort after recieving headers
            tries = 0
            maxtries = 100
            while not line.startswith("magnet:?"):
                line = f.readline()
                if not line:
                    tries = maxtries + 1 # fixme: really? we can do better than this
                    break
                tries += 1
                if tries > maxtries:
                    print("Found assumed magnet archive, skipping validity check...")
                    break
            if tries > maxtries:
                continue
            try:
                print("Sending request to " + line.replace("\n", "") + "...")
                r = requests.get(line, stream=True, timeout=10)
                if not r.status_code in range(200, 300):
                    print("Removing " + dir + "...")
                    f.close()
                    os.remove(dir)
            except:
                print("Removing " + dir + "...")
                f.close()
                os.remove(dir)

print("Loading archive contents...")
fuzzset = FuzzySet(use_levenshtein=False, rel_sim_cutoff=0.3) # 0.3 to get matches with lots of differing parts
searchpath = "./archives"
if not os.path.exists(searchpath):
    os.makedirs(searchpath)
for file in os.listdir(searchpath):
    if file.endswith(".txt") and not file.startswith("_"):
        print("Loading " + file + "...")
        with open(os.path.join("./archives", file), "r", errors='replace') as f:
            for line in f.read().splitlines():
                fuzzset.add(line)
            f.close()

def search_func(query, config):
    results = fuzzset.get(query)
    final = []
    for result in results:
        print(result)
        final.append(str(result[1]))
    return final