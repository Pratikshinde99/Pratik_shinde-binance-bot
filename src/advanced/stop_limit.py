"""
Stop-Limit Order implementation for Binance Futures
Triggers a limit order when stop price is reached
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.exceptions import BinanceAPIException
from base_bot import BasicBot
from logger import logger
from validator import Validator, ValidationError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class StopLimitBot(BasicBot):
    """Bot for executing stop-limit orders"""
    
    def place_stop_limit_order(self, symbol, side, quantity, stop_price, limit_price, time_in_force='GTC'):
        """
        Place a stop-limit order
        
        When market price reaches stop_price, a limit order is placed at limit_price
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            quantity: Order quantity
            stop_price: Price that triggers the limit order
            limit_price: Limit price for the order once triggered
            time_in_force: GTC (Good Till Cancel), IOC, FOK
            
        Returns:
            Order response dict
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            side = Validator.validate_side(side)
            quantity = Validator.validate_quantity(quantity)
            stop_price = Validator.validate_price(stop_price)
            limit_price = Validator.validate_price(limit_price)
            time_in_force = Validator.validate_time_in_force(time_in_force)
            
            # Log order attempt
            logger.log_order('STOP_LIMIT', symbol, side, quantity, limit_price)
            logger.info(f"Stop price: {stop_price}")
            
            # Get current price for reference
            current_price = self.get_current_price(symbol)
            logger.info(f"Current market price: {current_price}")
            
            # Validate stop price logic
            if side == 'BUY' and stop_price <= current_price:
                raise ValidationError(
                    f"For BUY stop-limit, stop price ({stop_price}) must be above current price ({current_price})"
                )
            elif side == 'SELL' and stop_price >= current_price:
                raise ValidationError(
                    f"For SELL stop-limit, stop price ({stop_price}) must be below current price ({current_price})"
                )
            
            # Place stop-limit order
            logger.log_api_call("newOrder", {
                "symbol": symbol,
                "side": side,
                "type": "STOP",
                "quantity": quantity,
                "price": limit_price,
                "stopPrice": stop_price,
                "timeInForce": time_in_force
            })
            
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP',
                quantity=quantity,
                price=limit_price,
                stopPrice=stop_price,
                timeInForce=time_in_force
            )
            
            # Log successful order
            logger.log_order('STOP_LIMIT', symbol, side, quantity, limit_price, order['status'])
            logger.log_api_response(order)
            
            # Print success message
            print(f"\n{Fore.GREEN}✓ Stop-Limit Order Placed Successfully!{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Order ID:{Style.RESET_ALL} {order['orderId']}")
            print(f"{Fore.CYAN}Symbol:{Style.RESET_ALL} {order['symbol']}")
            print(f"{Fore.CYAN}Side:{Style.RESET_ALL} {order['side']}")
            print(f"{Fore.CYAN}Quantity:{Style.RESET_ALL} {order['origQty']}")
            print(f"{Fore.CYAN}Stop Price:{Style.RESET_ALL} {order['stopPrice']}")
            print(f"{Fore.CYAN}Limit Price:{Style.RESET_ALL} {order['price']}")
            print(f"{Fore.CYAN}Current Price:{Style.RESET_ALL} {current_price}")
            print(f"{Fore.CYAN}Status:{Style.RESET_ALL} {order['status']}")
            print(f"{Fore.CYAN}Time in Force:{Style.RESET_ALL} {order['timeInForce']}")
            
            print(f"\n{Fore.YELLOW}How it works:{Style.RESET_ALL}")
            print(f"  When market price reaches {stop_price}, a limit order will be placed at {limit_price}")
            
            return order
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
            
        except BinanceAPIException as e:
            logger.log_error_trace(e, "Binance API error placing stop-limit order")
            print(f"\n{Fore.RED}✗ API Error:{Style.RESET_ALL} {e.message}")
            raise
            
        except Exception as e:
            logger.log_error_trace(e, "Unexpected error placing stop-limit order")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for stop-limit orders"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - Stop-Limit Order Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    # Check command line arguments
    if len(sys.argv) < 6:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python stop_limit.py <SYMBOL> <SIDE> <QUANTITY> <STOP_PRICE> <LIMIT_PRICE> [TIME_IN_FORCE]")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python stop_limit.py BTCUSDT BUY 0.01 51000 51500")
        print(f"  python stop_limit.py ETHUSDT SELL 0.1 2900 2850 GTC")
        print(f"\n{Fore.CYAN}Arguments:{Style.RESET_ALL}")
        print(f"  SYMBOL        - Trading pair (e.g., BTCUSDT, ETHUSDT)")
        print(f"  SIDE          - BUY or SELL")
        print(f"  QUANTITY      - Order quantity")
        print(f"  STOP_PRICE    - Price that triggers the limit order")
        print(f"  LIMIT_PRICE   - Limit price once triggered")
        print(f"  TIME_IN_FORCE - GTC (default), IOC, or FOK (optional)")
        print(f"\n{Fore.CYAN}Use Cases:{Style.RESET_ALL}")
        print(f"  • Stop-Loss: SELL when price drops to stop price")
        print(f"  • Buy Breakout: BUY when price rises above resistance")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    quantity = sys.argv[3]
    stop_price = sys.argv[4]
    limit_price = sys.argv[5]
    time_in_force = sys.argv[6] if len(sys.argv) > 6 else 'GTC'
    
    try:
        # Initialize bot
        print(f"{Fore.CYAN}Initializing bot...{Style.RESET_ALL}")
        bot = StopLimitBot(testnet=True)
        
        # Display account info
        balance = bot.get_account_balance()
        print(f"\n{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT")
        print(f"{Fore.GREEN}Available Balance:{Style.RESET_ALL} {balance['available_balance']} USDT\n")
        
        # Place stop-limit order
        print(f"{Fore.CYAN}Placing stop-limit order...{Style.RESET_ALL}")
        order = bot.place_stop_limit_order(
            symbol, side, float(quantity), 
            float(stop_price), float(limit_price), 
            time_in_force
        )
        
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
