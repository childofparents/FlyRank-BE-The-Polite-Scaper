import os
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Constants
CACHE_DIR = "cache"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/childofparents/FlyRank-BE-The-Polite-Scaper)"
TIMEOUT_SECONDS = 5
DELAY_SECONDS = 0.5
MAX_PAGES = 3


def get_html(url, filename):
    """Fetches HTML from cache or network with politeness."""
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)

    cache_file = os.path.join(CACHE_DIR, filename)

    if os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read()

    # If not cached, respect the delay before hitting the network
    time.sleep(DELAY_SECONDS)

    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT_SECONDS)
        if response.status_code == 200:
            html = response.text
            with open(cache_file, "w", encoding="utf-8") as f:
                f.write(html)
            return html
        else:
            print(f"Failed to fetch {url}. Status: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed for {url}: {e}")
        return None


def discover_book_urls():
    """Crawls up to MAX_PAGES catalogue pages and extracts book URLs."""
    current_url = START_URL
    pages_crawled = 0
    all_discovered_urls = []

    while current_url and pages_crawled < MAX_PAGES:
        pages_crawled += 1
        filename = f"catalogue-page-{pages_crawled}.html"

        html = get_html(current_url, filename)
        if not html:
            break

        soup = BeautifulSoup(html, "html.parser")

        # Extract book links on the current page
        for article in soup.find_all("article", class_="product_pod"):
            h3 = article.find("h3")
            if h3:
                a_tag = h3.find("a")
                if a_tag and "href" in a_tag.attrs:
                    relative_url = a_tag["href"]
                    absolute_url = urljoin(current_url, relative_url)
                    all_discovered_urls.append(absolute_url)

        # Find the 'next' button for pagination
        next_button = soup.select_one("li.next a")
        if next_button and "href" in next_button.attrs:
            current_url = urljoin(current_url, next_button["href"])
        else:
            current_url = None

    # Deduplicate URLs
    unique_urls = list(set(all_discovered_urls))

    print(f"catalogue_pages = {pages_crawled}")
    print(f"discovered = {len(all_discovered_urls)}")
    print(f"unique_urls = {len(unique_urls)}")

    return unique_urls


def main():
    print("Starting Stage 2 discovery...")
    discover_book_urls()


if __name__ == "__main__":
    main()