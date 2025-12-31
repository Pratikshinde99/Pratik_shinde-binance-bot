"""
Limit Order implementation for Binance Futures
Places orders at specified price levels
"""
import sys
from binance.exceptions import BinanceAPIException
from base_bot import BasicBot
from logger import logger
from validator import Validator, ValidationError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class LimitOrderBot(BasicBot):
    """Bot for executing limit orders"""
    
    def place_limit_order(self, symbol, side, quantity, price, time_in_force='GTC'):
        """
        Place a limit order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            price: Limit price
            time_in_force: GTC (Good Till Cancel), IOC (Immediate or Cancel), FOK (Fill or Kill)
            
        Returns:
            Order response dict
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            side = Validator.validate_side(side)
            quantity = Validator.validate_quantity(quantity)
            price = Validator.validate_price(price)
            time_in_force = Validator.validate_time_in_force(time_in_force)
            
            # Log order attempt
            logger.log_order('LIMIT', symbol, side, quantity, price)
            
            # Get current price for reference
            current_price = self.get_current_price(symbol)
            logger.info(f"Current market price: {current_price}")
            logger.info(f"Limit price: {price}")
            
            # Calculate price difference
            price_diff_pct = ((price - current_price) / current_price) * 100
            logger.info(f"Price difference: {price_diff_pct:.2f}%")
            
            # Place limit order
            logger.log_api_call("newOrder", {
                "symbol": symbol,
                "side": side,
                "type": "LIMIT",
                "quantity": quantity,
                "price": price,
                "timeInForce": time_in_force
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='LIMIT',
                quantity=quantity,
                price=price,
                timeInForce=time_in_force
            )
            
            # Log successful order
            logger.log_order('LIMIT', symbol, side, quantity, price, order['status'])
            logger.log_api_response(order)
            
            # Print success message
            print(f"\n{Fore.GREEN}✓ Limit Order Placed Successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Order ID:{Style.RESET_ALL} {order['orderId']}")
            print(f"{Fore.CYAN}Symbol:{Style.RESET_ALL} {order['symbol']}")
            print(f"{Fore.CYAN}Side:{Style.RESET_ALL} {order['side']}")
            print(f"{Fore.CYAN}Quantity:{Style.RESET_ALL} {order['origQty']}")
            print(f"{Fore.CYAN}Limit Price:{Style.RESET_ALL} {order['price']}")
            print(f"{Fore.CYAN}Current Price:{Style.RESET_ALL} {current_price}")
            print(f"{Fore.CYAN}Price Difference:{Style.RESET_ALL} {price_diff_pct:.2f}%")
            print(f"{Fore.CYAN}Status:{Style.RESET_ALL} {order['status']}")
            print(f"{Fore.CYAN}Time in Force:{Style.RESET_ALL} {order['timeInForce']}")
            
            return order
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
            
        except BinanceAPIException as e:
            logger.log_error_trace(e, "Binance API error placing limit order")
            print(f"\n{Fore.RED}✗ API Error:{Style.RESET_ALL} {e.message}")
            raise
            
        except Exception as e:
            logger.log_error_trace(e, "Unexpected error placing limit order")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for limit orders"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - Limit Order Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    # Check command line arguments
    if len(sys.argv) < 5:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python limit_orders.py <SYMBOL> <SIDE> <QUANTITY> <PRICE> [TIME_IN_FORCE]")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python limit_orders.py BTCUSDT BUY 0.01 50000")
        print(f"  python limit_orders.py ETHUSDT SELL 0.1 3000 GTC")
        print(f"\n{Fore.CYAN}Arguments:{Style.RESET_ALL}")
        print(f"  SYMBOL        - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print(f"  SIDE          - BUY or SELL")
        print(f"  QUANTITY      - Order quantity (decimal allowed)")
        print(f"  PRICE         - Limit price")
        print(f"  TIME_IN_FORCE - GTC (default), IOC, or FOK (optional)")
        print(f"\n{Fore.CYAN}Time in Force:{Style.RESET_ALL}")
        print(f"  GTC - Good Till Cancel (remains until filled or cancelled)")
        print(f"  IOC - Immediate or Cancel (fill immediately or cancel)")
        print(f"  FOK - Fill or Kill (fill completely or cancel)")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    quantity = sys.argv[3]
    price = sys.argv[4]
    time_in_force = sys.argv[5] if len(sys.argv) > 5 else 'GTC'
    
    try:
        # Initialize bot
        print(f"{Fore.CYAN}Initializing bot...{Style.RESET_ALL}")
        bot = LimitOrderBot(testnet=True)
        
        # Display account info
        balance = bot.get_account_balance()
        print(f"\n{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT")
        print(f"{Fore.GREEN}Available Balance:{Style.RESET_ALL} {balance['available_balance']} USDT\n")
        
        # Place limit order
        print(f"{Fore.CYAN}Placing limit order...{Style.RESET_ALL}")
        order = bot.place_limit_order(symbol, side, float(quantity), float(price), time_in_force)
        
        print(f"\n{Fore.GREEN}Order placed successfully!{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Note:{Style.RESET_ALL} This is a limit order. It will be filled when the market price reaches your limit price.")
        print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Fore.RED}Failed to execute order{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    main()
