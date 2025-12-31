"""
Logging module for Binance Futures Trading Bot
Provides structured logging with timestamps and error traces
"""
import logging
import sys
from pathlib import Path
from config import Config

class BotLogger:
    """Custom logger for trading bot operations"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotLogger, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
            
        self._initialized = True
        self.logger = logging.getLogger('BinanceFuturesBot')
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).parent.parent
        log_file = log_dir / Config.LOG_FILE
        
        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            Config.LOG_FORMAT,
            datefmt=Config.LOG_DATE_FORMAT
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        # Add handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message):
        """Log info message"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log debug message"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log warning message"""
        self.logger.warning(message)
    
    def error(self, message, exc_info=False):
        """Log error message with optional exception trace"""
        self.logger.error(message, exc_info=exc_info)
    
    def critical(self, message, exc_info=False):
        """Log critical message with optional exception trace"""
        self.logger.critical(message, exc_info=exc_info)
    
    def log_order(self, order_type, symbol, side, quantity, price=None, status='PENDING'):
        """Log order placement"""
        msg = f"ORDER [{order_type}] {side} {quantity} {symbol}"
        if price:
            msg += f" @ {price}"
        msg += f" - Status: {status}"
        self.info(msg)
    
    def log_api_call(self, endpoint, params=None):
        """Log API call"""
        msg = f"API CALL: {endpoint}"
        if params:
            msg += f" | Params: {params}"
        self.debug(msg)
    
    def log_api_response(self, response_data):
        """Log API response"""
        self.debug(f"API RESPONSE: {response_data}")
    
    def log_error_trace(self, error, context=""):
        """Log error with full trace"""
        msg = f"ERROR: {context} - {str(error)}" if context else f"ERROR: {str(error)}"
        self.error(msg, exc_info=True)

# Global logger instance
logger = BotLogger()
