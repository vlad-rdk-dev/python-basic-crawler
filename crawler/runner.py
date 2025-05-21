import asyncio
import json
from urllib.parse import urljoin, urldefrag, urlparse

import httpx
from bs4 import BeautifulSoup

import os
import json
from datetime import datetime,UTC
from slugify import slugify

from crawler.storage import discovered_pages, crawl_lock, reset_storage

MAX_DEPTH = 4
MAX_CONCURRENCY = 10

async def run_crawl(start_url: str) -> dict:
    if crawl_lock.acquire(blocking=False):
        try:
            reset_storage()
            return await crawl(start_url)
        finally:
            crawl_lock.release()
    else:
        raise RuntimeError("A crawl is already in progress.")



async def crawl(start_url: str) -> dict:
    parsed = urlparse(start_url)
    base_domain = parsed.netloc

    queue = asyncio.Queue()
    visited = set()

    await queue.put((start_url, 0))

    async with httpx.AsyncClient() as client:
        semaphore = asyncio.Semaphore(MAX_CONCURRENCY)

        async def worker():
            while not queue.empty():
                current_url, depth = await queue.get()

                if current_url in visited or depth > MAX_DEPTH:
                    continue

                visited.add(current_url)
                discovered_pages.add(current_url)

                #print(f"[Crawler] Visiting {current_url} at depth {depth}")

                async with semaphore:
                    links = await fetch_links(client, current_url, base_domain)

                for link in links:
                    if link not in visited:
                        await queue.put((link, depth + 1))

        workers = [asyncio.create_task(worker()) for _ in range(MAX_CONCURRENCY)]
        await asyncio.gather(*workers)

    result = {
        "domain": start_url,
        "pages": sorted(discovered_pages)
    }
    print(json.dumps(result, indent=2))

    #Create directory
    os.makedirs("results", exist_ok=True)

    #Generate filename
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S")
    safe_name = slugify(start_url)
    filename = f"results/{safe_name}-{timestamp}.json"

    #Write to file
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"[Crawler] Result saved to {filename}")
    except Exception as e:
        print(f"[Crawler] Failed to save result to {filename}: {e}")

    return result


async def fetch_links(client: httpx.AsyncClient, url: str, base_domain: str) -> list[str]:
    try:
        response = await client.get(url, timeout=10, follow_redirects=True)

        soup = BeautifulSoup(response.text, "html.parser")
        links = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            full_url = urldefrag(urljoin(url, href)).url
            parsed = urlparse(full_url)

            # Normalize: remove trailing slashes only if it's not the root page
            if full_url != parsed.scheme + "://" + parsed.netloc + "/":
                full_url = full_url.rstrip("/")

            # Filter for same domain/subdomain
            if parsed.netloc.endswith(base_domain):
                links.append(full_url)

        return links
    except Exception as e:
        print(f"[Crawler] Error fetching {url}: {e}")
        return []
