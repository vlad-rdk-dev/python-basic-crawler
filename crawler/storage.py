from threading import Lock

# Set to store discovered page URLs
discovered_pages: set[str] = set()

# Lock to allow only one crawl at a time
crawl_lock = Lock()

def reset_storage() -> None:
    """
    Clears the stored pages before starting a new crawl.
    """
    discovered_pages.clear()
