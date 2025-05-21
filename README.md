# Async Web Crawler with FastAPI

This project crawls all pages of a given website and returns a list of discovered URLs via a REST API.

## Features

- FastAPI backend
- Asynchronous crawling with `httpx` and `asyncio`
- HTML parsing with `BeautifulSoup`
- URL normalization and deduplication
- Optional - results saved to JSON file

## Setup

1. **Clone the repository**
2. Install dependencies: pip install -r requirements.txt
3. Run API on local host: uvicorn main:app --reload
