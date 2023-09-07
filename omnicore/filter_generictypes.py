def book_filter(results, config):
    exts = ["txt", "epub", "pdf", "mobi", "azw", "azw3", "djvu", "fb2", "ibooks", "lit", "pdb", "prc", "ps", "rtf", "tcr"]
    return [r for r in results if r.split(".")[-1].lower() in exts]

def video_filter(results, config):
    exts = ["mp4", "mkv", "avi", "mov", "wmv", "flv", "webm", "mpg", "mpeg", "m4v", "3gp", "3g2", "m2v", "m4v", "m2ts", "mts", "ts", "vob"]
    return [r for r in results if r.split(".")[-1].lower() in exts]