from . import searcher_localarchive
from . import filter_ddlalive

modules = {
    "searchers": [
        {
            "name": "Local Archive",
            "desc": "Scans local text files containing URLs seperated by newlines. Good for use with pre-existing legacy odsearcher archives.",
            "func": searcher_localarchive.search_func
        }
    ],
    "filters": [
        {
            "name": "DDL Alive",
            "desc": "Makes sure DDL links are alive",
            "func": filter_ddlalive.filter_func
        }
    ],
    "sorters": []
}