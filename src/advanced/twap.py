"""
TWAP (Time-Weighted Average Price) Order implementation
Splits large orders into smaller chunks over time
"""
import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.exceptions import BinanceAPIException
from base_bot import BasicBot
from logger import logger
from validator import Validator, ValidationError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TWAPBot(BasicBot):
    """Bot for executing TWAP orders"""
    
    def execute_twap_order(self, symbol, side, total_quantity, num_orders, interval_seconds):
        """
        Execute a TWAP order by splitting into smaller market orders over time
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL
            total_quantity: Total quantity to trade
            num_orders: Number of orders to split into
            interval_seconds: Time interval between orders (in seconds)
            
        Returns:
            List of executed orders
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            side = Validator.validate_side(side)
            total_quantity = Validator.validate_quantity(total_quantity)
            
            if num_orders < 2:
                raise ValidationError("Number of orders must be at least 2")
            if num_orders > 100:
                raise ValidationError("Number of orders cannot exceed 100")
            if interval_seconds < 1:
                raise ValidationError("Interval must be at least 1 second")
            
            # Calculate order size
            order_size = total_quantity / num_orders
            order_size = Validator.validate_quantity(order_size)
            
            logger.info(f"Starting TWAP order: {total_quantity} {symbol} split into {num_orders} orders")
            logger.info(f"Order size: {order_size}, Interval: {interval_seconds}s")
            
            print(f"\n{Fore.CYAN}TWAP Order Configuration:{Style.RESET_ALL}")
            print(f"  Symbol: {symbol}")
            print(f"  Side: {side}")
            print(f"  Total Quantity: {total_quantity}")
            print(f"  Number of Orders: {num_orders}")
            print(f"  Order Size: {order_size}")
            print(f"  Interval: {interval_seconds} seconds")
            print(f"  Total Duration: {(num_orders - 1) * interval_seconds} seconds\n")
            
            executed_orders = []
            total_filled = 0
            
            for i in range(num_orders):
                try:
                    # Adjust last order to account for rounding
                    if i == num_orders - 1:
                        remaining = total_quantity - total_filled
                        current_order_size = remaining
                    else:
                        current_order_size = order_size
                    
                    print(f"{Fore.YELLOW}[{i+1}/{num_orders}]{Style.RESET_ALL} Placing order for {current_order_size} {symbol}...")
                    
                    # Place market order
                    order = self.client.futures_create_order(
                        symbol=symbol,
                        side=side,
                        type='MARKET',
                        quantity=current_order_size
                    )
                    
                    executed_orders.append(order)
                    filled_qty = float(order['executedQty'])
                    total_filled += filled_qty
                    
                    logger.log_order('TWAP', symbol, side, current_order_size, status='FILLED')
                    logger.info(f"TWAP order {i+1}/{num_orders} filled: {filled_qty}")
                    
                    print(f"{Fore.GREEN}✓ Order {i+1} filled: {filled_qty} @ Market{Style.RESET_ALL}")
                    
                    # Wait before next order (except for last order)
                    if i < num_orders - 1:
                        print(f"{Fore.CYAN}Waiting {interval_seconds} seconds...{Style.RESET_ALL}\n")
                        time.sleep(interval_seconds)
                    
                except BinanceAPIException as e:
                    logger.error(f"Error placing TWAP order {i+1}: {e.message}")
                    print(f"{Fore.RED}✗ Error on order {i+1}: {e.message}{Style.RESET_ALL}")
                    break
            
            # Summary
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}TWAP Execution Complete{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Total Orders Executed:{Style.RESET_ALL} {len(executed_orders)}/{num_orders}")
            print(f"{Fore.CYAN}Total Quantity Filled:{Style.RESET_ALL} {total_filled}/{total_quantity}")
            
            if executed_orders:
                avg_price = sum(float(o.get('avgPrice', 0)) for o in executed_orders) / len(executed_orders)
                print(f"{Fore.CYAN}Average Execution Price:{Style.RESET_ALL} {avg_price}")
            
            logger.info(f"TWAP execution complete: {len(executed_orders)} orders, {total_filled} filled")
            
            return executed_orders
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Error executing TWAP order")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for TWAP orders"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - TWAP Order Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    if len(sys.argv) < 6:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python twap.py <SYMBOL> <SIDE> <TOTAL_QTY> <NUM_ORDERS> <INTERVAL_SEC>")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python twap.py BTCUSDT BUY 0.1 10 30")
        print(f"  python twap.py ETHUSDT SELL 1.0 5 60")
        print(f"\n{Fore.CYAN}Arguments:{Style.RESET_ALL}")
        print(f"  SYMBOL       - Trading pair")
        print(f"  SIDE         - BUY or SELL")
        print(f"  TOTAL_QTY    - Total quantity to trade")
        print(f"  NUM_ORDERS   - Number of orders to split into (2-100)")
        print(f"  INTERVAL_SEC - Seconds between orders")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    total_quantity = sys.argv[3]
    num_orders = sys.argv[4]
    interval_seconds = sys.argv[5]
    
    try:
        bot = TWAPBot(testnet=True)
        balance = bot.get_account_balance()
        print(f"{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT\n")
        
        orders = bot.execute_twap_order(
            symbol, side, float(total_quantity),
            int(num_orders), int(interval_seconds)
        )
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
        sys.exit(0)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
