# FlyRank Internship A9: The Polite Scraper

## Target Classification
* **Target Site:** [Books to Scrape](https://books.toscrape.com/) (toscrape.com)
* **Why this site:** It is a public practice sandbox explicitly built so people can practice scraping on it.
* **Scope:** The first 3 catalogue pages only.
* **Data Collected:** Book details including titles, prices, ratings, and descriptions.
* **Robots.txt check:** No robots file found.

**I will not reuse this code on another site without checking its rules and terms first.**

## Setup and Execution
This scraper is built in the Python lane. 

**Installation:**
```bash
pip install requests beautifulsoup4 pydantic
```
**Run command from the root directory:**
```bash
python src/main.py
```

## Record Schema
The final normalized records follow this schema:
* title (String)
* product_url (Absolute URL)
* price_text (Original string, e.g., "£51.77")
* price_gbp (Numeric float, e.g., 51.77)
* availability_text (String)
* rating_text (String, Optional)
* description (String, Optional)
* source_page (Absolute URL indicating provenance)
* fetched_at (UTC Timestamp)

## Politeness Rules
This scraper acts as a polite guest by strictly enforcing the following rules:
* **User-Agent**: Identifies itself honestly using `FlyRankInternship-A9/1.0 (+https://github.com/childofparents/FlyRank-BE-The-Polite-Scaper)`.
* **Delay**: Waits at least 0.5 seconds between real network requests.
* **Timeout**: Limits network requests to 5 seconds to prevent hanging.
* **Caching**: Saves successful HTML responses locally. Subsequent runs read from the disk rather than querying the live server.

## Limitation
**Brittle Selectors**: The HTML parsing relies on specific class names and HTML structures. If the site's layout changes, the BeautifulSoup selectors will fail and need to be updated.

## Architecture Note: Why No Browser?
The target data is already fully present in the raw HTML that the server sends upon the initial request. Firing up a headless browser (like Playwright or Selenium) to render JavaScript would only add unnecessary execution time, memory overhead, and compute cost.

## Ethical Considerations
I commit to using official APIs whenever they are available. I will never attempt to bypass logins, paywalls, or active blocks, and I will strictly collect only the data necessary for the task at hand.

### Proof of Execution
Below is a real `run-report.json` generated from a successful run, proving cache utilization, schema validation, and the survival of one deliberately injected broken page:
```JSON
{
  "start_time": "2026-08-10T20:44:09Z",
  "duration_seconds": 0.99,
  "pages_fetched": 1,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```
