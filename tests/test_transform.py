import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
import utils.transform as transform

class TestTransformData(unittest.TestCase):
    def test_transform_basic(self):
        raw_data = [
            {
                "Title": "Cool Shoes",
                "Price": "$50",
                "Rating": "4.5 /5",
                "Colors": "Color: 3",
                "Size": "Size: 42",
                "Gender": "Gender: Male"
            },
            {
                "Title": "Unknown Product",
                "Price": "Price Unavailable",
                "Rating": "Invalid Rating /5",
                "Colors": "Color: 2",
                "Size": "Size: 40",
                "Gender": "Gender: Female"
            },
            {
                "Title": "Nice Hat",
                "Price": "$20",
                "Rating": "Not Rated",
                "Colors": "Color: 1",
                "Size": "Size: M",
                "Gender": "Gender: Unisex"
            },
            {
                "Title": "Cool Shoes",
                "Price": "$50",
                "Rating": "4.5 /5",
                "Colors": "Color: 3",
                "Size": "Size: 42",
                "Gender": "Gender: Male"
            },
            {
                "Title": "Valid Product",
                "Price": "$10",
                "Rating": "3.0 /5",
                "Colors": "Color: 2",
                "Size": "Size: S",
                "Gender": "Gender: Female"
            },
            {
                "Title": "Null Color",
                "Price": "$30",
                "Rating": "4.0 /5",
                "Colors": "Color: 0",
                "Size": "Size: L",
                "Gender": "Gender: Male"
            }
        ]

        for d in raw_data:
            if d["Colors"] is None:
                d["Colors"] = "Color: 0"
            elif isinstance(d["Colors"], int):
                d["Colors"] = f"Color: {d['Colors']}"
            else:
                d["Colors"] = str(d["Colors"])

        df = transform.transform_data(raw_data)
        self.assertEqual(len(df), 3)  

        # Mengecek harga sudah konversi ke IDR
        self.assertAlmostEqual(df.loc[df['Title'] == 'Cool Shoes', 'Price'].values[0], 50 * 16000)
        self.assertAlmostEqual(df.loc[df['Title'] == 'Valid Product', 'Price'].values[0], 10 * 16000)
        self.assertAlmostEqual(df.loc[df['Title'] == 'Null Color', 'Price'].values[0], 30 * 16000)

        # Mengecek rating sudah jadi float
        self.assertEqual(df.loc[df['Title'] == 'Cool Shoes', 'Rating'].values[0], 4.5)
        self.assertEqual(df.loc[df['Title'] == 'Valid Product', 'Rating'].values[0], 3.0)
        self.assertEqual(df.loc[df['Title'] == 'Null Color', 'Rating'].values[0], 4.0)

        # Mengecek Colors sudah jadi int
        self.assertEqual(df.loc[df['Title'] == 'Cool Shoes', 'Colors'].values[0], 3)
        self.assertEqual(df.loc[df['Title'] == 'Valid Product', 'Colors'].values[0], 2)
        self.assertEqual(df.loc[df['Title'] == 'Null Color', 'Colors'].values[0], 0)

        # Mengecek Size dan Gender sudah bersih tanpa prefix
        self.assertEqual(df.loc[df['Title'] == 'Cool Shoes', 'Size'].values[0], "42")
        self.assertEqual(df.loc[df['Title'] == 'Cool Shoes', 'Gender'].values[0], "Male")

        self.assertEqual(df.loc[df['Title'] == 'Valid Product', 'Size'].values[0], "S")
        self.assertEqual(df.loc[df['Title'] == 'Valid Product', 'Gender'].values[0], "Female")

        self.assertEqual(df.loc[df['Title'] == 'Null Color', 'Size'].values[0], "L")
        self.assertEqual(df.loc[df['Title'] == 'Null Color', 'Gender'].values[0], "Male")

