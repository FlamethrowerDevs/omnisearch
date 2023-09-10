# Extending Omnisearch's Functionality

Omnisearch works through a multitude of omnicore modules which all interface with different services. There are three types of modules that all influence search results:

## Developing a Module

### Module Structure

Every module is a simple Python file that contains at least one function, which can be named practically anything. This function must accept the following arguments, depending on what it is your module does:

- For searchers, the function must accept a string, `query`, and a dictionary, `config`. The function must return a list of URLs (as strings), `results`.
- For filters, the function must accept a list of URLs (as strings), `results`, and a dictionary, `config`. The function must return a list of URLs (as strings), `results`.
- For sorters, the function must accept a list of URLs (as strings), `results`, a dictionary, `config`, and a string, `query`. The function must return a list of URLs (as strings), `results`.

For example, a searcher module for a publicly available API might look like this:

```python
import requests

def search_func(query, config):
    results = []
    response = requests.get('https://api.example.com/search', params={'q': query})
    for result in response.json():
        results.append(result['url'])
    return results
```

### Module Configuration

Once you've created an omnicore module, you just have to add it to the `modules.py` file (and optionally, the `__init__.py` file to make it a default option). An entry in `modules.py` could look like this:

```python
from . import searcher_mycoolsearcher

# ...

{
    "name": "My Cool Searcher",
    "id"  : "coolsearcher",
    "desc": "Calls api.example.com for results.",
    "func": searcher_mycoolsearcher.search_func
},
```

To add the module to the default options, add an entry in the respective list in `__init__.py`:

```python
import json
from . import modules

# ...

def dosearch(query, config):
    print("[omnicore] Searching for: " + query)
    try:
        config = json.loads(config)
    except:
        config = {"sorters": ["..."], "filters": ["..."], "searchers": ["...", "My Cool Searcher"]} # default config
# ...
```
