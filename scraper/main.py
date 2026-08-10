import os
import time
import requests
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, timezone

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
    """Crawls up to MAX_PAGES catalogue pages and extracts book URLs and their sources."""
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

        for article in soup.find_all("article", class_="product_pod"):
            h3 = article.find("h3")
            if h3:
                a_tag = h3.find("a")
                if a_tag and "href" in a_tag.attrs:
                    relative_url = a_tag["href"]
                    absolute_url = urljoin(current_url, relative_url)
                    all_discovered_urls.append({
                        "url": absolute_url,
                        "source": current_url
                    })

        next_button = soup.select_one("li.next a")
        if next_button and "href" in next_button.attrs:
            current_url = urljoin(current_url, next_button["href"])
        else:
            current_url = None

    unique_urls = {}
    for item in all_discovered_urls:
        if item["url"] not in unique_urls:
            unique_urls[item["url"]] = item["source"]

    print(f"catalogue_pages = {pages_crawled}")
    print(f"discovered = {len(all_discovered_urls)}")
    print(f"unique_urls = {len(unique_urls)}")

    return unique_urls


def extract_book_details(book_links):
    """Visits each book page, extracts raw data, and maintains provenance."""
    raw_records = []

    for product_url, source_page in book_links.items():
        # Create a safe, unique filename based on the book's URL slug
        folder_slug = product_url.strip("/").split("/")[-2]
        filename = f"book-{folder_slug}.html"

        html = get_html(product_url, filename)
        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")
        product_main = soup.find("div", class_="col-sm-6 product_main")

        # Extract fields
        title = product_main.find("h1").text if product_main and product_main.find("h1") else None

        price_tag = product_main.find("p", class_="price_color")
        price = price_tag.text if price_tag else None

        availability_tag = product_main.find("p", class_="availability")
        availability = availability_tag.text.strip() if availability_tag else None

        rating_tag = product_main.find("p", class_="star-rating")
        rating = rating_tag["class"][1] if rating_tag and len(rating_tag["class"]) > 1 else None

        # Description is outside the product_main div
        description = None
        desc_heading = soup.find("div", id="product_description")
        if desc_heading:
            desc_paragraph = desc_heading.find_next_sibling("p")
            if desc_paragraph:
                description = desc_paragraph.text

        fetched_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        record = {
            "title": title,
            "product_url": product_url,
            "price_text": price,
            "availability_text": availability,
            "rating_text": rating,
            "description": description,
            "source_page": source_page,
            "fetched_at": fetched_at
        }

        raw_records.append(record)

    print(f"detail_pages = {len(raw_records)}")

    # Print the first complete record as proof
    if raw_records:
        print(json.dumps(raw_records[0], indent=2))

    return raw_records


def main():
    print("Starting Stage 2 discovery...")
    book_links = discover_book_urls()

    print("\nStarting Stage 3 extraction...")
    extract_book_details(book_links)


if __name__ == "__main__":
    main()
