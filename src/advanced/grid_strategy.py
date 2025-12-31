"""
Grid Trading Strategy implementation
Automated buy-low/sell-high within a price range
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

class GridBot(BasicBot):
    """Bot for executing grid trading strategy"""
    
    def setup_grid_orders(self, symbol, lower_price, upper_price, num_grids, quantity_per_grid):
        """
        Setup grid trading orders within a price range
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            lower_price: Lower bound of price range
            upper_price: Upper bound of price range
            num_grids: Number of grid levels
            quantity_per_grid: Quantity for each grid order
            
        Returns:
            Dict with buy and sell orders
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            lower_price = Validator.validate_price(lower_price)
            upper_price = Validator.validate_price(upper_price)
            quantity_per_grid = Validator.validate_quantity(quantity_per_grid)
            
            if lower_price >= upper_price:
                raise ValidationError("Lower price must be less than upper price")
            if num_grids < 2:
                raise ValidationError("Number of grids must be at least 2")
            if num_grids > 50:
                raise ValidationError("Number of grids cannot exceed 50")
            
            # Get current price
            current_price = self.get_current_price(symbol)
            logger.info(f"Current price: {current_price}")
            
            if current_price < lower_price or current_price > upper_price:
                logger.warning(f"Current price {current_price} is outside grid range [{lower_price}, {upper_price}]")
            
            # Calculate grid levels
            price_step = (upper_price - lower_price) / (num_grids - 1)
            grid_levels = [lower_price + (i * price_step) for i in range(num_grids)]
            
            logger.info(f"Setting up grid: {num_grids} levels from {lower_price} to {upper_price}")
            logger.info(f"Price step: {price_step}")
            
            print(f"\n{Fore.CYAN}Grid Configuration:{Style.RESET_ALL}")
            print(f"  Symbol: {symbol}")
            print(f"  Price Range: {lower_price} - {upper_price}")
            print(f"  Current Price: {current_price}")
            print(f"  Number of Grids: {num_grids}")
            print(f"  Price Step: {price_step:.2f}")
            print(f"  Quantity per Grid: {quantity_per_grid}\n")
            
            buy_orders = []
            sell_orders = []
            
            # Place buy orders below current price
            print(f"{Fore.GREEN}Placing BUY orders below current price...{Style.RESET_ALL}")
            for level in grid_levels:
                if level < current_price:
                    try:
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side='BUY',
                            type='LIMIT',
                            quantity=quantity_per_grid,
                            price=level,
                            timeInForce='GTC'
                        )
                        buy_orders.append(order)
                        logger.info(f"BUY order placed at {level}")
                        print(f"  {Fore.GREEN}✓{Style.RESET_ALL} BUY @ {level} - Order ID: {order['orderId']}")
                    except BinanceAPIException as e:
                        logger.error(f"Failed to place BUY order at {level}: {e.message}")
                        print(f"  {Fore.RED}✗{Style.RESET_ALL} BUY @ {level} - Error: {e.message}")
            
            # Place sell orders above current price
            print(f"\n{Fore.YELLOW}Placing SELL orders above current price...{Style.RESET_ALL}")
            for level in grid_levels:
                if level > current_price:
                    try:
                        order = self.client.futures_create_order(
                            symbol=symbol,
                            side='SELL',
                            type='LIMIT',
                            quantity=quantity_per_grid,
                            price=level,
                            timeInForce='GTC'
                        )
                        sell_orders.append(order)
                        logger.info(f"SELL order placed at {level}")
                        print(f"  {Fore.YELLOW}✓{Style.RESET_ALL} SELL @ {level} - Order ID: {order['orderId']}")
                    except BinanceAPIException as e:
                        logger.error(f"Failed to place SELL order at {level}: {e.message}")
                        print(f"  {Fore.RED}✗{Style.RESET_ALL} SELL @ {level} - Error: {e.message}")
            
            # Summary
            print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.GREEN}Grid Setup Complete{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
            print(f"{Fore.CYAN}BUY Orders Placed:{Style.RESET_ALL} {len(buy_orders)}")
            print(f"{Fore.CYAN}SELL Orders Placed:{Style.RESET_ALL} {len(sell_orders)}")
            print(f"{Fore.CYAN}Total Orders:{Style.RESET_ALL} {len(buy_orders) + len(sell_orders)}")
            
            logger.info(f"Grid setup complete: {len(buy_orders)} BUY, {len(sell_orders)} SELL orders")
            
            return {
                'buy_orders': buy_orders,
                'sell_orders': sell_orders,
                'grid_levels': grid_levels
            }
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Error setting up grid")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for grid trading"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - Grid Trading Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    if len(sys.argv) < 6:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python grid_strategy.py <SYMBOL> <LOWER_PRICE> <UPPER_PRICE> <NUM_GRIDS> <QTY_PER_GRID>")
        print(f"\n{Fore.CYAN}Examples:{Style.RESET_ALL}")
        print(f"  python grid_strategy.py BTCUSDT 48000 52000 10 0.001")
        print(f"  python grid_strategy.py ETHUSDT 2800 3200 5 0.01")
        print(f"\n{Fore.CYAN}Arguments:{Style.RESET_ALL}")
        print(f"  SYMBOL        - Trading pair")
        print(f"  LOWER_PRICE   - Lower bound of grid")
        print(f"  UPPER_PRICE   - Upper bound of grid")
        print(f"  NUM_GRIDS     - Number of grid levels (2-50)")
        print(f"  QTY_PER_GRID  - Quantity for each grid order")
        sys.exit(1)
    
    symbol = sys.argv[1]
    lower_price = sys.argv[2]
    upper_price = sys.argv[3]
    num_grids = sys.argv[4]
    quantity_per_grid = sys.argv[5]
    
    try:
        bot = GridBot(testnet=True)
        balance = bot.get_account_balance()
        print(f"{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT\n")
        
        result = bot.setup_grid_orders(
            symbol, float(lower_price), float(upper_price),
            int(num_grids), float(quantity_per_grid)
        )
        
        print(f"\n{Fore.YELLOW}Grid is now active and will trade automatically!{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
        sys.exit(0)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
