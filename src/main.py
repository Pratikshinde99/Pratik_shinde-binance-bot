"""
Main CLI interface for Binance Futures Trading Bot
Provides interactive menu for all order types
"""
import sys
import os
from colorama import Fore, Style, init
from config import Config
from base_bot import BasicBot
from logger import logger

# Initialize colorama
init(autoreset=True)

def print_banner():
    """Print bot banner"""
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'':^70}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'Binance Futures Trading Bot':^70}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'Testnet Mode':^70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'':^70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

def print_menu():
    """Print main menu"""
    print(f"\n{Fore.YELLOW}Available Order Types:{Style.RESET_ALL}\n")
    print(f"{Fore.GREEN}Core Orders:{Style.RESET_ALL}")
    print(f"  1. Market Order     - Execute at current market price")
    print(f"  2. Limit Order      - Place order at specific price\n")
    
    print(f"{Fore.CYAN}Advanced Orders:{Style.RESET_ALL}")
    print(f"  3. Stop-Limit       - Trigger limit order at stop price")
    print(f"  4. OCO Order        - One-Cancels-the-Other (TP + SL)")
    print(f"  5. TWAP Strategy    - Time-Weighted Average Price")
    print(f"  6. Grid Trading     - Automated buy-low/sell-high\n")
    
    print(f"{Fore.MAGENTA}Account & Info:{Style.RESET_ALL}")
    print(f"  7. View Balance     - Check account balance")
    print(f"  8. View Positions   - Check open positions")
    print(f"  9. View Orders      - Check open orders\n")
    
    print(f"  0. Exit\n")

def run_market_order():
    """Run market order"""
    from market_orders import MarketOrderBot
    
    print(f"\n{Fore.YELLOW}=== Market Order ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    side = input("Side (BUY/SELL): ").strip()
    quantity = input("Quantity: ").strip()
    
    try:
        bot = MarketOrderBot(testnet=True)
        bot.place_market_order(symbol, side, float(quantity))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def run_limit_order():
    """Run limit order"""
    from limit_orders import LimitOrderBot
    
    print(f"\n{Fore.YELLOW}=== Limit Order ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    side = input("Side (BUY/SELL): ").strip()
    quantity = input("Quantity: ").strip()
    price = input("Limit Price: ").strip()
    tif = input("Time in Force (GTC/IOC/FOK) [GTC]: ").strip() or "GTC"
    
    try:
        bot = LimitOrderBot(testnet=True)
        bot.place_limit_order(symbol, side, float(quantity), float(price), tif)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def run_stop_limit():
    """Run stop-limit order"""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'advanced'))
    from advanced.stop_limit import StopLimitBot
    
    print(f"\n{Fore.YELLOW}=== Stop-Limit Order ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    side = input("Side (BUY/SELL): ").strip()
    quantity = input("Quantity: ").strip()
    stop_price = input("Stop Price: ").strip()
    limit_price = input("Limit Price: ").strip()
    
    try:
        bot = StopLimitBot(testnet=True)
        bot.place_stop_limit_order(symbol, side, float(quantity), 
                                   float(stop_price), float(limit_price))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def run_oco():
    """Run OCO order"""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'advanced'))
    from advanced.oco import OCOBot
    
    print(f"\n{Fore.YELLOW}=== OCO Order ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    side = input("Side (BUY/SELL): ").strip()
    quantity = input("Quantity: ").strip()
    tp_price = input("Take Profit Price: ").strip()
    sl_price = input("Stop Loss Price: ").strip()
    
    try:
        bot = OCOBot(testnet=True)
        bot.place_oco_order(symbol, side, float(quantity), 
                           float(tp_price), float(sl_price))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def run_twap():
    """Run TWAP strategy"""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'advanced'))
    from advanced.twap import TWAPBot
    
    print(f"\n{Fore.YELLOW}=== TWAP Strategy ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    side = input("Side (BUY/SELL): ").strip()
    total_qty = input("Total Quantity: ").strip()
    num_orders = input("Number of Orders: ").strip()
    interval = input("Interval (seconds): ").strip()
    
    try:
        bot = TWAPBot(testnet=True)
        bot.execute_twap_order(symbol, side, float(total_qty), 
                              int(num_orders), int(interval))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def run_grid():
    """Run grid trading"""
    sys.path.append(os.path.join(os.path.dirname(__file__), 'advanced'))
    from advanced.grid_strategy import GridBot
    
    print(f"\n{Fore.YELLOW}=== Grid Trading ==={Style.RESET_ALL}\n")
    symbol = input("Symbol (e.g., BTCUSDT): ").strip()
    lower = input("Lower Price: ").strip()
    upper = input("Upper Price: ").strip()
    num_grids = input("Number of Grids: ").strip()
    qty_per_grid = input("Quantity per Grid: ").strip()
    
    try:
        bot = GridBot(testnet=True)
        bot.setup_grid_orders(symbol, float(lower), float(upper), 
                             int(num_grids), float(qty_per_grid))
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def view_balance():
    """View account balance"""
    try:
        bot = BasicBot(testnet=True)
        balance = bot.get_account_balance()
        
        print(f"\n{Fore.GREEN}=== Account Balance ==={Style.RESET_ALL}\n")
        print(f"Total Balance:      {balance['total_balance']} USDT")
        print(f"Available Balance:  {balance['available_balance']} USDT")
        print(f"Unrealized PnL:     {balance['total_unrealized_profit']} USDT")
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def view_positions():
    """View open positions"""
    try:
        bot = BasicBot(testnet=True)
        positions = bot.get_position_info()
        
        print(f"\n{Fore.GREEN}=== Open Positions ==={Style.RESET_ALL}\n")
        if not positions:
            print("No open positions")
        else:
            for pos in positions:
                print(f"Symbol: {pos['symbol']}")
                print(f"  Position: {pos['positionAmt']}")
                print(f"  Entry Price: {pos['entryPrice']}")
                print(f"  Unrealized PnL: {pos['unRealizedProfit']}")
                print()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def view_orders():
    """View open orders"""
    try:
        bot = BasicBot(testnet=True)
        orders = bot.get_open_orders()
        
        print(f"\n{Fore.GREEN}=== Open Orders ==={Style.RESET_ALL}\n")
        if not orders:
            print("No open orders")
        else:
            for order in orders:
                print(f"Order ID: {order['orderId']}")
                print(f"  Symbol: {order['symbol']}")
                print(f"  Side: {order['side']}")
                print(f"  Type: {order['type']}")
                print(f"  Price: {order.get('price', 'N/A')}")
                print(f"  Quantity: {order['origQty']}")
                print()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")

def main():
    """Main CLI loop"""
    print_banner()
    
    # Check configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"{Fore.RED}Configuration Error:{Style.RESET_ALL} {e}")
        print(f"\nPlease set up your .env file with API credentials.")
        print(f"See .env.example for reference.")
        sys.exit(1)
    
    menu_actions = {
        '1': run_market_order,
        '2': run_limit_order,
        '3': run_stop_limit,
        '4': run_oco,
        '5': run_twap,
        '6': run_grid,
        '7': view_balance,
        '8': view_positions,
        '9': view_orders,
    }
    
    while True:
        try:
            print_menu()
            choice = input(f"{Fore.CYAN}Select option (0-9): {Style.RESET_ALL}").strip()
            
            if choice == '0':
                print(f"\n{Fore.YELLOW}Exiting... Goodbye!{Style.RESET_ALL}\n")
                break
            
            if choice in menu_actions:
                menu_actions[choice]()
            else:
                print(f"{Fore.RED}Invalid option. Please try again.{Style.RESET_ALL}")
            
            input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
            
        except KeyboardInterrupt:
            print(f"\n\n{Fore.YELLOW}Exiting... Goodbye!{Style.RESET_ALL}\n")
            break
        except Exception as e:
            logger.log_error_trace(e, "Main loop error")
            print(f"{Fore.RED}Unexpected error: {e}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
