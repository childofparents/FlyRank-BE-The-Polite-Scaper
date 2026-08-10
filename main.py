import os
import requests

# Constants
CACHE_DIR = "cache"
PAGE_1_URL = "https://books.toscrape.com/catalogue/category/books_1/page-1.html"
CACHE_FILE = os.path.join(CACHE_DIR, "catalogue-page-1.html")
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/childofparents/FlyRank-BE-The-Polite-Scaper)"
TIMEOUT_SECONDS = 5


def fetch_first_page():
    """Fetches the first catalogue page or reads from cache if it exists."""

    # Ensure cache directory exists
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    # Check for cached file
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            html = f.read()
        print(f"CACHE HIT: {len(html)} bytes")
        return html

    # If not cached, fetch from the web
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(PAGE_1_URL, headers=headers, timeout=TIMEOUT_SECONDS)

        # Check status code
        if response.status_code == 200:
            html = response.text
            # Save to cache
            with open(CACHE_FILE, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"FETCH: {len(html)} bytes")
            return html
        else:
            print(f"Failed to fetch. Status code: {response.status_code}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None


def main():
    fetch_first_page()


if __name__ == "__main__":
    main()