import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import requests
import utils.extract as extract
from unittest.mock import patch, MagicMock
from bs4 import BeautifulSoup
from datetime import datetime
from unittest.mock import patch, Mock
from utils.extract import fetching_content, extract_product, scrape_product

class TestExtract(unittest.TestCase):
    @patch("utils.extract.requests.Session")
    def test_fetching_content_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test</body></html>"
        mock_get.return_value.get.return_value = mock_response
        
        result = fetching_content("https://fashion-studio.dicoding.dev/?page={}")
        
        self.assertEqual(result, b"<html><body>Test</body></html>")

class TestExtractUtils(unittest.TestCase):
    @patch("utils.extract.requests.Session")
    def test_fetching_content_fail(self, mock_session):
        mock_instance = mock_session.return_value
        mock_instance.get.side_effect = Exception("Failed to fetch")
        
        with self.assertRaises(Exception):
            extract.fetching_content("https://fashion-studio.dicoding.dev/?page={} ")

    def test_extract_product(self):
        html = """
        <div class="collection-card">
            <h3 class="product-title">Sepatu Sport</h3>
            <span class="price">$50</span>
            <p>Rating: 4.0</p>
            <p>Color: Red, Blue</p>
            <p>Size: 42</p>
            <p>Gender: Unisex</p>
        </div>
        """
        soup = BeautifulSoup(html, "html.parser")
        card = soup.find("div", class_="collection-card")
        product = extract.extract_product(card)

        self.assertEqual(product["Title"], "Sepatu Sport")
        self.assertEqual(product["Price"], "$50")
        self.assertEqual(product["Rating"], "Rating: 4.0")
        self.assertEqual(product["Colors"], "Color: Red, Blue")
        self.assertEqual(product["Size"], "Size: 42")
        self.assertEqual(product["Gender"], "Gender: Unisex")
        self.assertIn("Timestamp", product)

class TestScrapeProduct(unittest.TestCase):
    @patch("utils.extract.fetching_content")
    @patch("time.sleep", return_value=None)
    def test_scrape_product_50_pages(self, mock_sleep, mock_fetching_content):
        sample_html = """
        <main class="container">
            <div class="collection-grid">
                <div class="collection-card">
                    <h3 class="product-title">Sepatu Sport</h3>
                    <span class="price">$50</span>
                    <p>Rating: 4.0</p>
                    <p>Color: Red, Blue</p>
                    <p>Size: 42</p>
                    <p>Gender: Unisex</p>
                </div>
            </div>
        </main>
        """
        mock_fetching_content.return_value = sample_html.encode('utf-8')

        results = extract.scrape_product("https://fashion-studio.dicoding.dev", start_page=1, delay=0)

        self.assertEqual(len(results), 50)

        # mengecek salah satu produk
        product = results[0]
        self.assertEqual(product["Title"], "Sepatu Sport")
        self.assertEqual(product["Price"], "$50")
        self.assertEqual(product["Rating"], "Rating: 4.0")
        self.assertEqual(product["Colors"], "Color: Red, Blue")
        self.assertEqual(product["Size"], "Size: 42")
        self.assertEqual(product["Gender"], "Gender: Unisex")
        self.assertIn("Timestamp", product)

        # fetching_content memanggil halaman pertama
        mock_fetching_content.assert_any_call("https://fashion-studio.dicoding.dev")