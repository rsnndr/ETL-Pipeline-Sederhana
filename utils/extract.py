import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0"
    )
}

def fetching_content(url):
    """Mengambil konten HTML dari URL yang diberikan."""
    session = requests.Session()
    response = session.get(url, headers=HEADERS)
    try:
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan ketika melakukan request terhadap {url}: {e}")
        return None

def extract_product(card):
    """Mengambil data produk berupa title, price, colors, size, dan gender dari elemen card (HTML)."""
    title_elem = card.find("h3", class_="product-title")
    price_elem = card.find("span", class_="price")
    info_paragraphs = card.find_all("p")

    # untuk menghindari error
    title = title_elem.text.strip() if title_elem else None
    price = price_elem.text.strip() if price_elem else None
    rating, colors, size, gender = None, None, None, None

    # untuk mendeteksi atribut produk
    for p in info_paragraphs:
        text = p.text.strip().lower()
        if "rating" in text:
            rating = p.text.strip()
        elif "color" in text:
            colors = p.text.strip()
        elif "size" in text:
            size = p.text.strip()
        elif "gender" in text:
            gender = p.text.strip()

    product = {
        "Title": title,
        "Price": price,
        "Rating": rating,
        "Colors": colors,
        "Size": size,
        "Gender": gender,
        "Rating": rating,
        "Timestamp": datetime.now().isoformat()
    }

    return product

def scrape_product(base_url, start_page=1, delay=2): 
    """Fungsi utama untuk mengambil keseluruhan data"""
    data = []

    for page in range(start_page, 51):
        # Format URL halaman
        url = base_url if page == 1 else f"{base_url}/page{page}"
        print(f"Scraping halaman: {url}")
        
        content = fetching_content(url)
        soup = BeautifulSoup(content, "html.parser")
        main = soup.find('main', class_='container')
        product_grid = main.find('div', class_='collection-grid')
        cards = product_grid.find_all('div', class_='collection-card')
        
        for card in cards:
            product = extract_product(card)
            data.append(product)

        time.sleep(delay)  

    return data    