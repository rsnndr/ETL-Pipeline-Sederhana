#TRANSFORM
import pandas as pd
import re
 
def transform_data(data):
    df = pd.DataFrame(data)
 
    # menghapus data kotor
    dirty_patterns = {
        "Title": ["Unknown Product"],
        "Rating": ["Invalid Rating /5", "Not Rated"],
        "Price": ["Price Unavailable", None]
    }
    for column, patterns in dirty_patterns.items():
        for pattern in patterns:
            df = df[~df[column].str.contains(re.escape(str(pattern)), na=False, case=False)]
 
    # mengonversi harga dolar ke rupiah
    def convert_price(price_str):
        price_number = re.sub(r"[^0-9.]", "", price_str)
        return float(price_number) * 16000 if price_number else None
    df["Price"] = df["Price"].apply(convert_price)
 
    # membersihkan rating
    def clean_rating(rating_str):
        match = re.search(r"([0-9.]+)", rating_str)
        return float(match.group(1)) if match else None
    df["Rating"] = df["Rating"].apply(clean_rating)
 
    # Bersihkan colors
    def clean_colors(colors_str):
        match = re.search(r"(\d+)", colors_str)
        return int(match.group(1)) if match else None
    df["Colors"] = df["Colors"].apply(clean_colors)
 
    # membersihkan size dan gender
    df["Size"] = df["Size"].str.replace("Size:", "", regex=False).str.strip()
    df["Gender"] = df["Gender"].str.replace("Gender:", "", regex=False).str.strip()
 
    # menghapus duplikat dan null
    df = df.drop_duplicates()
    df = df.dropna()
 
    return df