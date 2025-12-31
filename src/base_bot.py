"""
Base bot class for Binance Futures trading
Provides core functionality for all order types
"""
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException
from config import Config
from logger import logger
from validator import Validator, ValidationError

class BasicBot:
    """Base trading bot with core Binance Futures functionality"""
    
    def __init__(self, api_key=None, api_secret=None, testnet=True):
        """
        Initialize the trading bot
        
        Args:
            api_key: Binance API key (optional, reads from config if not provided)
            api_secret: Binance API secret (optional, reads from config if not provided)
            testnet: Use testnet (default: True)
        """
        self.api_key = api_key or Config.API_KEY
        self.api_secret = api_secret or Config.API_SECRET
        self.testnet = testnet
        
        # Validate credentials
        if not self.api_key or not self.api_secret:
            raise ValueError("API credentials not provided")
        
        # Initialize Binance client
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            
            # Set testnet URL if using testnet
            if self.testnet:
                self.client.API_URL = 'https://testnet.binancefuture.com'
            
            # Sync timestamp with server to avoid timestamp errors
            try:
                server_time = self.client.get_server_time()
                import time
                local_time = int(time.time() * 1000)
                time_offset = server_time['serverTime'] - local_time
                self.client.timestamp_offset = time_offset
                logger.debug(f"Timestamp offset set to {time_offset}ms")
            except:
                # If timestamp sync fails, continue without it
                pass
            
            logger.info(f"Bot initialized - Testnet: {self.testnet}")
            
            # Test connection
            self._test_connection()
            
        except Exception as e:
            logger.log_error_trace(e, "Failed to initialize bot")
            raise
    
    def _test_connection(self):
        """Test API connection"""
        try:
            logger.log_api_call("ping")
            self.client.futures_ping()
            logger.info("API connection successful")
            
            # Get account info
            logger.log_api_call("account")
            account = self.client.futures_account()
            balance = float(account['totalWalletBalance'])
            logger.info(f"Account Balance: {balance} USDT")
            
        except BinanceAPIException as e:
            logger.log_error_trace(e, "API connection failed")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Connection test failed")
            raise
    
    def get_symbol_info(self, symbol):
        """
        Get symbol information and trading rules
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Symbol information dict
        """
        try:
            symbol = Validator.validate_symbol(symbol)
            logger.log_api_call("exchangeInfo", {"symbol": symbol})
            
            exchange_info = self.client.futures_exchange_info()
            
            for s in exchange_info['symbols']:
                if s['symbol'] == symbol:
                    logger.debug(f"Symbol info retrieved: {symbol}")
                    return s
            
            raise ValueError(f"Symbol not found: {symbol}")
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, f"Failed to get symbol info for {symbol}")
            raise
    
    def get_current_price(self, symbol):
        """
        Get current market price for a symbol
        
        Args:
            symbol: Trading pair symbol
            
        Returns:
            Current price as float
        """
        try:
            symbol = Validator.validate_symbol(symbol)
            logger.log_api_call("ticker/price", {"symbol": symbol})
            
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            
            logger.debug(f"Current price for {symbol}: {price}")
            return price
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, f"Failed to get price for {symbol}")
            raise
    
    def get_account_balance(self):
        """
        Get account balance
        
        Returns:
            Account balance information
        """
        try:
            logger.log_api_call("account")
            account = self.client.futures_account()
            
            balance_info = {
                'total_balance': float(account['totalWalletBalance']),
                'available_balance': float(account['availableBalance']),
                'total_unrealized_profit': float(account['totalUnrealizedProfit'])
            }
            
            logger.info(f"Account Balance: {balance_info['total_balance']} USDT")
            return balance_info
            
        except Exception as e:
            logger.log_error_trace(e, "Failed to get account balance")
            raise
    
    def set_leverage(self, symbol, leverage):
        """
        Set leverage for a symbol
        
        Args:
            symbol: Trading pair symbol
            leverage: Leverage multiplier (1-125)
            
        Returns:
            Leverage setting response
        """
        try:
            symbol = Validator.validate_symbol(symbol)
            leverage = Validator.validate_leverage(leverage)
            
            logger.log_api_call("leverage", {"symbol": symbol, "leverage": leverage})
            
            response = self.client.futures_change_leverage(
                symbol=symbol,
                leverage=leverage
            )
            
            logger.info(f"Leverage set to {leverage}x for {symbol}")
            logger.log_api_response(response)
            
            return response
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except BinanceAPIException as e:
            logger.log_error_trace(e, f"Failed to set leverage for {symbol}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Unexpected error setting leverage")
            raise
    
    def get_open_orders(self, symbol=None):
        """
        Get all open orders
        
        Args:
            symbol: Trading pair symbol (optional, gets all if not provided)
            
        Returns:
            List of open orders
        """
        try:
            params = {}
            if symbol:
                symbol = Validator.validate_symbol(symbol)
                params['symbol'] = symbol
            
            logger.log_api_call("openOrders", params)
            orders = self.client.futures_get_open_orders(**params)
            
            logger.info(f"Retrieved {len(orders)} open orders")
            return orders
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Failed to get open orders")
            raise
    
    def cancel_order(self, symbol, order_id):
        """
        Cancel an open order
        
        Args:
            symbol: Trading pair symbol
            order_id: Order ID to cancel
            
        Returns:
            Cancellation response
        """
        try:
            symbol = Validator.validate_symbol(symbol)
            
            logger.log_api_call("cancel", {"symbol": symbol, "orderId": order_id})
            
            response = self.client.futures_cancel_order(
                symbol=symbol,
                orderId=order_id
            )
            
            logger.info(f"Order {order_id} cancelled for {symbol}")
            logger.log_api_response(response)
            
            return response
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except BinanceAPIException as e:
            logger.log_error_trace(e, f"Failed to cancel order {order_id}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Unexpected error cancelling order")
            raise
    
    def get_position_info(self, symbol=None):
        """
        Get position information
        
        Args:
            symbol: Trading pair symbol (optional)
            
        Returns:
            Position information
        """
        try:
            params = {}
            if symbol:
                symbol = Validator.validate_symbol(symbol)
                params['symbol'] = symbol
            
            logger.log_api_call("positionRisk", params)
            positions = self.client.futures_position_information(**params)
            
            # Filter out positions with zero amount
            active_positions = [p for p in positions if float(p['positionAmt']) != 0]
            
            logger.info(f"Retrieved {len(active_positions)} active positions")
            return active_positions
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Failed to get position info")
            raise
