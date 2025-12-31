"""
Final comprehensive test of the Binance Futures Trading Bot
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from base_bot import BasicBot
from colorama import Fore, Style, init

init(autoreset=True)

def print_header(title):
    print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{title:^70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")

def print_success(message):
    print(f"{Fore.GREEN}✓ {message}{Style.RESET_ALL}")

def print_info(label, value):
    print(f"{Fore.YELLOW}{label}:{Style.RESET_ALL} {value}")

print_header("Binance Futures Trading Bot - Connection Test")

try:
    # Test 1: Initialize Bot
    print(f"{Fore.CYAN}Test 1: Initializing Bot...{Style.RESET_ALL}")
    bot = BasicBot(testnet=True)
    print_success("Bot initialized successfully!")
    print_success("Connected to Binance Futures Testnet")
    
    # Test 2: Get Account Balance
    print(f"\n{Fore.CYAN}Test 2: Fetching Account Information...{Style.RESET_ALL}")
    balance = bot.get_account_balance()
    print_success("Account information retrieved")
    print_info("  Total Balance", f"{balance['total_balance']:,.2f} USDT")
    print_info("  Available Balance", f"{balance['available_balance']:,.2f} USDT")
    print_info("  Unrealized PnL", f"{balance['total_unrealized_profit']:+,.2f} USDT")
    
    # Test 3: Get Current Prices
    print(f"\n{Fore.CYAN}Test 3: Fetching Market Prices...{Style.RESET_ALL}")
    btc_price = bot.get_current_price('BTCUSDT')
    eth_price = bot.get_current_price('ETHUSDT')
    print_success("Market prices retrieved")
    print_info("  BTC/USDT", f"${btc_price:,.2f}")
    print_info("  ETH/USDT", f"${eth_price:,.2f}")
    
    # Test 4: Get Open Orders
    print(f"\n{Fore.CYAN}Test 4: Checking Open Orders...{Style.RESET_ALL}")
    orders = bot.get_open_orders()
    print_success(f"Found {len(orders)} open orders")
    
    # Test 5: Get Positions
    print(f"\n{Fore.CYAN}Test 5: Checking Open Positions...{Style.RESET_ALL}")
    positions = bot.get_position_info()
    print_success(f"Found {len(positions)} active positions")
    
    # Final Summary
    print_header("✓ ALL TESTS PASSED!")
    
    print(f"{Fore.GREEN}Your Binance Futures Trading Bot is ready!{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}API Configuration:{Style.RESET_ALL}")
    print(f"  ✓ API credentials configured correctly")
    print(f"  ✓ Connection to testnet successful")
    print(f"  ✓ Account accessible")
    print(f"  ✓ Market data available")
    
    print(f"\n{Fore.CYAN}Next Steps:{Style.RESET_ALL}")
    print(f"  1. Try the interactive menu:")
    print(f"     {Fore.WHITE}cd src{Style.RESET_ALL}")
    print(f"     {Fore.WHITE}py main.py{Style.RESET_ALL}")
    print()
    print(f"  2. Test a market order (small amount):")
    print(f"     {Fore.WHITE}cd src{Style.RESET_ALL}")
    print(f"     {Fore.WHITE}py market_orders.py BTCUSDT BUY 0.001{Style.RESET_ALL}")
    print()
    print(f"  3. Test a limit order:")
    print(f"     {Fore.WHITE}py limit_orders.py BTCUSDT BUY 0.001 45000{Style.RESET_ALL}")
    print()
    print(f"  4. Try advanced orders:")
    print(f"     {Fore.WHITE}cd advanced{Style.RESET_ALL}")
    print(f"     {Fore.WHITE}py oco.py BTCUSDT SELL 0.001 52000 48000{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}Documentation:{Style.RESET_ALL}")
    print(f"  • Quick Start: QUICKSTART.md")
    print(f"  • Full Guide: README.md")
    print(f"  • Complete Overview: COMPLETE_GUIDE.md")
    
    print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}\n")
    
except Exception as e:
    print(f"\n{Fore.RED}{'='*70}{Style.RESET_ALL}")
    print(f"{Fore.RED}✗ TEST FAILED{Style.RESET_ALL}")
    print(f"{Fore.RED}{'='*70}{Style.RESET_ALL}\n")
    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
    
    print(f"{Fore.YELLOW}Troubleshooting:{Style.RESET_ALL}")
    print(f"  1. Check .env file has correct API keys")
    print(f"  2. Verify keys from: https://testnet.binancefuture.com")
    print(f"  3. Ensure API key has Futures permissions")
    print(f"  4. Check internet connection")
    print()
    
    import traceback
    print(f"{Fore.YELLOW}Detailed Error:{Style.RESET_ALL}")
    traceback.print_exc()
    print()
