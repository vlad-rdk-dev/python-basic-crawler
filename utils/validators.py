from urllib.parse import urlparse

def is_valid_url(url: str) -> bool:
    """
    Basic validation to ensure the URL has a scheme and netloc.
    
    Args:
        url (str): URL to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    parsed = urlparse(url)
    return all([parsed.scheme in ("http", "https"), parsed.netloc])
