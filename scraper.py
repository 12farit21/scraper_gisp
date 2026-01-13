import requests
import json
import time
from database import init_db, insert_company, insert_product, get_product_count, get_company_count
from parser import parse_product, parse_company

# API configuration
API_URL = "https://gisp.gov.ru/mapm/api/product-list"

# Headers (обновлено на основе нового запроса)
HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru-KZ,ru;q=0.9",
    "Content-Type": "application/json",
    "Origin": "https://gisp.gov.ru",
    "Referer": "https://gisp.gov.ru/goods/",
    "Sec-Ch-Ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36",
    "X-Ajax-Token": "8887ad9c0cd09d86d04232551def7493a29e4216a96d783d6ebe87e54f6ba5c4",
    "x-csrftoken": "188a4758f3e21c2ecf6ab8e3bbc67c2ade84aeb61c53601c5c105482cfe56a4754362c29a7f68b27",
    "X-Requested-With": "XMLHttpRequest",
    # connection: keep-alive, host, content-length — requests сам добавляет, вручную не нужно
}

# Cookies (обновлено на основе cookie-заголовка из запроса)
COOKIES = {
    "nan-session": "188a47557b593848c81b9f55beb261f5977f13af8b60a7de94f3b22aece8fbf0a7ab0349c4d3de89e5c24e47ce4c49b3",
    "_ym_uid": "1768304239687420730",
    "_ym_d": "1768304239",
    "_pk_ses.1.8b63": "1",
    "_ym_isad": "2",
    "_pk_id.1.8b63": "ff26644f58eea63a.1768304241.1.1768304254.1768304241."
}

PER_PAGE = 96
DELAY_BETWEEN_REQUESTS = 1  # seconds

def fetch_page(page_number):
    """Fetch a single page of products from API"""
    payload = {
        "page": page_number,
        "per_page": PER_PAGE,
        "use_ai_search": True,
        "order": [
            {
                "field": "name",
                "direction": "asc"
            }
        ],
        "filters": {
            "status_code": "product"
        },
        "type": "[Product] Query"
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        cookies=COOKIES,
        data=json.dumps(payload),
        timeout=15
    )

    response.raise_for_status()
    return response.json()

def process_page(page_data):
    """Process a single page of products and save to database"""
    products_data = page_data.get('data', [])

    for product_json in products_data:
        # Parse and insert company first (to satisfy foreign key)
        company_data = parse_company(product_json)
        if company_data.get('id'):
            insert_company(company_data)

        # Parse and insert product
        product_data = parse_product(product_json)
        if product_data.get('id'):
            insert_product(product_data)

def run_scraper(start_page=1, max_pages=None):
    """Main scraper loop"""
    # Initialize database
    init_db()

    print("Starting GISP parser...")
    print(f"Configuration: per_page={PER_PAGE}, delay={DELAY_BETWEEN_REQUESTS}s")
    print()

    current_page = start_page
    total_products_saved = 0
    total_companies_saved = 0

    try:
        while True:
            if max_pages and current_page >= start_page + max_pages:
                break

            try:
                print(f"Fetching page {current_page}...", end="", flush=True)
                page_data = fetch_page(current_page)

                # Check if we got data
                products = page_data.get('data', [])
                if not products:
                    print(" No data received, stopping.")
                    break

                # Process products
                process_page(page_data)
                products_count = len(products)

                # Get current database counts
                total_products = get_product_count()
                total_companies = get_company_count()

                print(f" OK ({products_count} items) | DB: {total_products} products, {total_companies} companies")

                # Get last page info
                meta = page_data.get('meta', {})
                last_page = meta.get('last_page')

                if current_page >= last_page:
                    print(f"Reached last page ({last_page}), stopping.")
                    break

                # Delay before next request
                time.sleep(DELAY_BETWEEN_REQUESTS)
                current_page += 1

            except requests.exceptions.RequestException as e:
                print(f" ERROR: {e}")
                print(f"Retrying page {current_page} in 5 seconds...")
                time.sleep(5)
                continue

    except KeyboardInterrupt:
        print("\nScraper interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        raise

    # Final statistics
    final_products = get_product_count()
    final_companies = get_company_count()
    print()
    print("=" * 50)
    print(f"Scraping completed!")
    print(f"Total products: {final_products}")
    print(f"Total companies: {final_companies}")
    print("=" * 50)

if __name__ == "__main__":
    run_scraper()
