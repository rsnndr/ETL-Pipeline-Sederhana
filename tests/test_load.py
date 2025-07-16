import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import pandas as pd
from unittest.mock import patch, Mock, MagicMock
from utils.load import store_to_postgre, store_to_google_sheets, load_data

# Test Function untuk CSV
class TestLoadCsv(unittest.TestCase):
    def test_load_data_with_mock(self):
        mock_df = MagicMock()
        load_data(mock_df)
        mock_df.to_csv.assert_called_once_with("products.csv", index=False)

# Test Function untuk PostgreSQL
class TestLoadPostgre(unittest.TestCase):
    @patch("utils.load.create_engine")
    def test_store_to_postgre(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_connection = MagicMock()
        
        mock_engine.connect.return_value = mock_connection
        mock_connection.__enter__.return_value = mock_connection
        
        mock_create_engine.return_value = mock_engine
        
        mock_df = MagicMock()
        
        db_url = "postgresql://postgres:produk123@localhost/perusahaandb"
        store_to_postgre(mock_df, db_url)
        
        mock_create_engine.assert_called_once_with(db_url)
        mock_engine.connect.assert_called_once()
        mock_df.to_sql.assert_called_once_with('products', mock_engine, if_exists='replace', index=False)

# Test Function untuk GoogleSheet
class TestLoadGoogleSheet(unittest.TestCase):
    @patch("utils.load.build")
    def test_store_to_google_sheets(self, mock_build):
        mock_service = Mock()
        mock_sheets = Mock()
        mock_values = Mock()

        # Setup chaining mock
        mock_build.return_value = mock_service
        mock_service.spreadsheets.return_value = mock_sheets
        mock_sheets.values.return_value = mock_values
        mock_values.update.return_value.execute.return_value = {"updatedCells": 3}

        # memanggil fungsi yang akan di tes
        store_to_google_sheets(MagicMock())

        # memanggil method chaining
        mock_values.update.assert_called_once()
        args, kwargs = mock_values.update.call_args

        self.assertEqual(kwargs['spreadsheetId'], '16aaPDh9HGjpjHgt4nQwVdGLT8qvIxCMILuQpL6pS6d4')
        self.assertEqual(kwargs['range'], 'Sheet1!A2')
        self.assertEqual(kwargs['valueInputOption'], 'RAW')
        self.assertIn('values', kwargs['body'])
