"""
Test Data Reader utility module
Handles reading and parsing test data from JSON files
"""
import json
import os
from typing import Dict, Any
from utils.logger import Logger

logger = Logger.get_logger(__name__)


class TestDataReader:
    """Utility class to read test data from JSON files"""
    
    def __init__(self, data_file: str = 'test_data.json'):
        """
        Initialize TestDataReader
        
        Args:
            data_file: Name of the JSON data file (default: test_data.json)
        """
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.data_file_path = os.path.join(self.data_dir, data_file)
        self._data = None
        self._load_data()
    
    def _load_data(self) -> None:
        """Load test data from JSON file"""
        try:
            if not os.path.exists(self.data_file_path):
                raise FileNotFoundError(f"Test data file not found: {self.data_file_path}")
            
            with open(self.data_file_path, 'r', encoding='utf-8') as file:
                self._data = json.load(file)
                logger.info(f"Successfully loaded test data from: {self.data_file_path}")
        except FileNotFoundError as e:
            logger.error(f"Data file not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON format in data file: {e}")
            raise
        except Exception as e:
            logger.error(f"Error loading test data: {e}")
            raise
    
    def get_data(self, key: str = None) -> Any:
        """
        Get test data by key
        
        Args:
            key: Key to retrieve from test data. If None, returns all data
            
        Returns:
            Test data value or entire data dictionary
        """
        if key is None:
            return self._data
        
        try:
            keys = key.split('.')
            value = self._data
            for k in keys:
                value = value[k]
            logger.debug(f"Retrieved test data for key: {key}")
            return value
        except KeyError:
            logger.error(f"Key not found in test data: {key}")
            raise KeyError(f"Key '{key}' not found in test data")
    
    def get_user_credentials(self) -> Dict[str, str]:
        """
        Get user credentials from test data
        Generates unique email for each test run
        """
        from faker import Faker
        import time
        
        credentials = self.get_data('user_credentials').copy()
        
        # Generate unique email using timestamp and Faker
        fake = Faker()
        timestamp = str(int(time.time()))
        unique_username = f"testuser_{timestamp}_{fake.random_number(digits=4)}"
        credentials['email'] = f"{unique_username}@example.com"
        
        logger.info(f"Generated unique user credentials with email: {credentials['email']}")
        return credentials
    
    def get_billing_address(self) -> Dict[str, str]:
        """Get billing address from test data"""
        return self.get_data('billing_address')
    
    def get_shipping_address(self) -> Dict[str, str]:
        """Get shipping address from test data"""
        return self.get_data('shipping_address')
    
    def get_test_config(self) -> Dict[str, Any]:
        """Get test configuration from test data"""
        return self.get_data('test_config')
    
    def get_products_to_search(self) -> list:
        """Get list of products to search"""
        return self.get_data('products_to_search')

