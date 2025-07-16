import pandas as pd
import utils.load as load
import unittest
from utils.extract import scrape_product
from utils.transform import transform_data
from utils.load import load_data
from utils.load import store_to_postgre
from utils.load import store_to_google_sheets

def main():
    """Fungsi utama untuk keseluruhan proses scraping hingga menyimpannya."""
    BASE_URL = "https://fashion-studio.dicoding.dev/?page={}"

    # 1. Extract
    data = scrape_product("https://fashion-studio.dicoding.dev")

    # 2. Transform
    df = transform_data(data)

    # 3. Load
    load_data(df)
    
    # menyimpan data ke postgreSQL
    db_url = 'postgresql+psycopg2://products:produk123@localhost:5432/perusahaandb'
    store_to_postgre(df, db_url) # Memanggil fungsi untuk menyimpan ke database
    
    # menyimpan data ke Google Sheets
    store_to_google_sheets(df)

    # untuk menampilkan semua kolom
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)

    # 4. Cek duplikat
    print(f"Jumlah data duplikat: {df.duplicated().sum()}")

    # 5. Cek struktur kolom dan tipe data
    print("\nTipe data kolom:")
    print(df.dtypes)

    # 6. Cek info lengkap
    print("\nInfo DataFrame:")
    df.info()

    # 7. Cek 5 data pertama
    print("\nContoh 5 data pertama:")
    print(df.head())
    
if __name__ == "__main__":
    main()

