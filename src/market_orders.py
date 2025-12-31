"""
Market Order implementation for Binance Futures
Executes orders at current market price
"""
import sys
from binance.exceptions import BinanceAPIException
from base_bot import BasicBot
from logger import logger
from validator import Validator, ValidationError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class MarketOrderBot(BasicBot):
    """Bot for executing market orders"""
    
    def place_market_order(self, symbol, side, quantity):
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            
        Returns:
            Order response dict
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            side = Validator.validate_side(side)
            quantity = Validator.validate_quantity(quantity)
            
            # Log order attempt
            logger.log_order('MARKET', symbol, side, quantity)
            
            # Get current price for reference
            current_price = self.get_current_price(symbol)
            logger.info(f"Current market price: {current_price}")
            
            # Place market order
            logger.log_api_call("newOrder", {
                "symbol": symbol,
                "side": side,
                "type": "MARKET",
                "quantity": quantity
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='MARKET',
                quantity=quantity
            )
            
            # Log successful order
            logger.log_order('MARKET', symbol, side, quantity, 
                           current_price, 'FILLED')
            logger.log_api_response(order)
            
            # Print success message
            print(f"\n{Fore.GREEN}✓ Market Order Executed Successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Order ID:{Style.RESET_ALL} {order['orderId']}")
            print(f"{Fore.CYAN}Symbol:{Style.RESET_ALL} {order['symbol']}")
            print(f"{Fore.CYAN}Side:{Style.RESET_ALL} {order['side']}")
            print(f"{Fore.CYAN}Quantity:{Style.RESET_ALL} {order['origQty']}")
            print(f"{Fore.CYAN}Status:{Style.RESET_ALL} {order['status']}")
            
            if 'avgPrice' in order and order['avgPrice']:
                print(f"{Fore.CYAN}Average Price:{Style.RESET_ALL} {order['avgPrice']}")
            
            return order
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
            
        except BinanceAPIException as e:
            logger.log_error_trace(e, "Binance API error placing market order")
            print(f"\n{Fore.RED}✗ API Error:{Style.RESET_ALL} {e.message}")
            raise
            
        except Exception as e:
            logger.log_error_trace(e, "Unexpected error placing market order")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for market orders"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - Market Order Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    # Check command line arguments
    if len(sys.argv) < 4:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python market_orders.py <SYMBOL> <SIDE> <QUANTITY>")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python market_orders.py BTCUSDT BUY 0.01")
        print(f"  python market_orders.py ETHUSDT SELL 0.1")
        print(f"\n{Fore.CYAN}Arguments:{Style.RESET_ALL}")
        print(f"  SYMBOL   - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print(f"  SIDE     - BUY or SELL")
        print(f"  QUANTITY - Order quantity (decimal allowed)")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    quantity = sys.argv[3]
    
    try:
        # Initialize bot
        print(f"{Fore.CYAN}Initializing bot...{Style.RESET_ALL}")
        bot = MarketOrderBot(testnet=True)
        
        # Display account info
        balance = bot.get_account_balance()
        print(f"\n{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT")
        print(f"{Fore.GREEN}Available Balance:{Style.RESET_ALL} {balance['available_balance']} USDT\n")
        
        # Place market order
        print(f"{Fore.CYAN}Placing market order...{Style.RESET_ALL}")
        order = bot.place_market_order(symbol, side, float(quantity))
        
        print(f"\n{Fore.GREEN}Order placed successfully!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Failed to execute order{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
