from . import searcher_localarchive
from . import searcher_eyedex
from . import searcher_yts
from . import searcher_repacks
from . import searcher_odindexers
from . import searcher_libgen
from . import searcher_torrents
from . import filter_generictypes
from . import sorter_generic

modules = {
    "searchers": [
        {
            "name": "Local Archive",
            "desc": "Scans local text files containing URLs seperated by newlines. Good for use with pre-existing legacy odsearcher archives.",
            "func": searcher_localarchive.search_func
        },
        {
            "name": "The Eyedex",
            "desc": "Scans the Eyedex, an indexed version of the-eye.eu and other open directories on the web, totaling about 900tb. Great for books, popular media, other more obscure content, and NFOs.",
            "func": searcher_eyedex.search_func
        },
        {
            "name": "YTS/YIFY",
            "desc": "Scans yts.mx for torrents. Great for movies and TV shows in low file sizes. Long live the 2gb movie!",
            "func": searcher_yts.search_func
        },
        {
            "name": "Game Repackers",
            "desc": "Searches DODI and FitGirl repacks of games, which take the filesize of the download significantly lower.",
            "func": searcher_repacks.search_func
        },
        {
            "name": "Opendirectory Indexes",
            "desc": "Searches FilePursuit and odcrawler for all sorts of files found in unprotected open directories.",
            "func": searcher_odindexers.search_func
        },
        {
            "name": "Library Genesis",
            "desc": "Searches Library Genesis, more commonly referred to as libgen, for books, scholarly articles, and more.",
            "func": searcher_libgen.search_func
        },
        {
            "name": "Torrent Trackers",
            "desc": "Searches The Pirate Bay, 1337x, Limetorrents, and TorrentGalaxy for magnet links to torrents for all sorts of content.",
            "func": searcher_torrents.search_func
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
    "sorters": [
        {
            "name": "Fuzzy Match",
            "desc": "Sorts results by how closely they match the search query",
            "func": sorter_generic.fuzzy_sort
        }
    ],
    "forcedfilters": [
        {
            "name": "remove tpb empty res",
            "desc": "removes empty tpb responses with magnet:?xt=urn:btih:0000000000000000000000000000000000000000",
            "func": sorter_generic.remove_empty_tpb
        }
    ]
}