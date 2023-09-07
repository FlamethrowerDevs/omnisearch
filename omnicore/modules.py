from . import searcher_localarchive
from . import filter_generictypes

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
            "name": "Text",
            "desc": "Finds books or text files",
            "func": filter_generictypes.book_filter
        },
        {
            "name": "Video",
            "desc": "Finds video files",
            "func": filter_generictypes.video_filter
        },
        {
            "name": "Audio",
            "desc": "Finds audio files",
            "func": filter_generictypes.audio_filter
        },
        {
            "name": "Warez",
            "desc": "Finds warez, archives, and disk images",
            "func": filter_generictypes.warez_filter
        }
    ],
    "sorters": []
}