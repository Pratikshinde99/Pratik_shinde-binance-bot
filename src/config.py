"""
Configuration module for Binance Futures Trading Bot
Handles API credentials and testnet settings
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for bot settings"""
    
    # API Credentials
    API_KEY = os.getenv('BINANCE_API_KEY', '')
    API_SECRET = os.getenv('BINANCE_API_SECRET', '')
    
    # Testnet Settings
    TESTNET = os.getenv('TESTNET', 'True').lower() == 'true'
    TESTNET_BASE_URL = 'https://testnet.binancefuture.com'
    
    # Logging Settings
    LOG_FILE = 'bot.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    
    # Trading Settings
    DEFAULT_LEVERAGE = 10
    MAX_LEVERAGE = 125
    
    # Validation Settings
    MIN_QUANTITY = 0.001
    MAX_QUANTITY = 10000
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.API_KEY or not cls.API_SECRET:
            raise ValueError(
                "API credentials not found. Please set BINANCE_API_KEY and "
                "BINANCE_API_SECRET in .env file"
            )
        return True
