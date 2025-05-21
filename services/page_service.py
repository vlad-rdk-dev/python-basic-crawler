from utils.validators import is_valid_url
from crawler.runner import run_crawl

last_url: str | None = None

async def process_target_url(target_url: str) -> dict:
    if is_valid_url(target_url):
        print(f"URL to Crawl is: {target_url}")
        return await run_crawl(target_url)
    else:
        raise ValueError("Invalid URL format.")

    