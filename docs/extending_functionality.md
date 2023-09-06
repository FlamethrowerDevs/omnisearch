# Extending Omnisearch's Functionality

Omnisearch works through a multitude of modules which all interface with different services. There are three types of modules that all influence search results:

## Module Types

### Searcher Modules

These scrape sites, use APIs, and otherwise find the files. Some might operate on local indexes (like the odsearcher module), and others (like the filepursuit module) might operate on public sites that have limited or no API.

### Filter Modules

These modules filter out irrelevent results, such as those in incorrect languages, below a certain resolution threshold (for video and pictures), or otherwise sub-optimal files.

### Sorter Modules

These modules sort the final results from the searcher and filter modules into a more user-friendly format, pushing better results to the top of the results list in the WebUI.

## Managing Modules

Modules can be enabled or disabled at search-time by the user to further fine-tune search results. At least one searcher module must be enabled at all times, but other than that you can disable all other filtering.