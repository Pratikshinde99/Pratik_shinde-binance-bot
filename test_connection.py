"""
Quick test script to verify API connection with timestamp sync
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from binance.client import Client
from config import Config
from colorama import Fore, Style, init

init(autoreset=True)

print("\n" + "="*60)
print(f"{Fore.CYAN}Testing Binance Testnet Connection{Style.RESET_ALL}")
print("="*60 + "\n")

try:
    # Validate config
    print(f"{Fore.YELLOW}1. Checking API credentials...{Style.RESET_ALL}")
    Config.validate()
    print(f"{Fore.GREEN}   ✓ API credentials found in .env file{Style.RESET_ALL}\n")
    
    # Initialize client with timestamp offset
    print(f"{Fore.YELLOW}2. Connecting to Binance Testnet...{Style.RESET_ALL}")
    client = Client(Config.API_KEY, Config.API_SECRET, testnet=True)
    
    # Test ping
    print(f"{Fore.YELLOW}3. Testing API connection...{Style.RESET_ALL}")
    client.futures_ping()
    print(f"{Fore.GREEN}   ✓ Successfully connected to Binance Futures Testnet!{Style.RESET_ALL}\n")
    
    # Get server time
    print(f"{Fore.YELLOW}4. Syncing with server time...{Style.RESET_ALL}")
    server_time = client.futures_time()
    print(f"{Fore.GREEN}   ✓ Server time synced{Style.RESET_ALL}\n")
    
    # Get account info
    print(f"{Fore.YELLOW}5. Fetching account information...{Style.RESET_ALL}")
    account = client.futures_account()
    
    total_balance = float(account['totalWalletBalance'])
    available_balance = float(account['availableBalance'])
    unrealized_pnl = float(account['totalUnrealizedProfit'])
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Account Information:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"  Total Balance:      {total_balance:,.2f} USDT")
    print(f"  Available Balance:  {available_balance:,.2f} USDT")
    print(f"  Unrealized PnL:     {unrealized_pnl:+,.2f} USDT")
    
    # Get current prices
    print(f"\n{Fore.YELLOW}6. Fetching current market prices...{Style.RESET_ALL}")
    btc_ticker = client.futures_symbol_ticker(symbol='BTCUSDT')
    eth_ticker = client.futures_symbol_ticker(symbol='ETHUSDT')
    
    btc_price = float(btc_ticker['price'])
    eth_price = float(eth_ticker['price'])
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Current Market Prices:{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"  BTC/USDT: ${btc_price:,.2f}")
    print(f"  ETH/USDT: ${eth_price:,.2f}")
    
    print(f"\n{Fore.GREEN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ ALL TESTS PASSED!{Style.RESET_ALL}")
    print(f"{Fore.GREEN}{'='*60}{Style.RESET_ALL}\n")
    
    print(f"{Fore.CYAN}Your bot is ready to trade!{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Next steps:{Style.RESET_ALL}")
    print(f"  1. Interactive menu:  cd src && py main.py")
    print(f"  2. Market order test: cd src && py market_orders.py BTCUSDT BUY 0.001")
    print(f"  3. View documentation: README.md\n")
    
except ValueError as e:
    print(f"\n{Fore.RED}✗ Configuration Error!{Style.RESET_ALL}")
    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}\n")
    print(f"{Fore.YELLOW}Solution:{Style.RESET_ALL}")
    print(f"  1. Make sure .env file exists")
    print(f"  2. Add your API credentials to .env file")
    print(f"  3. Get API keys from: https://testnet.binancefuture.com\n")
    
except Exception as e:
    error_msg = str(e)
    print(f"\n{Fore.RED}✗ Connection Failed!{Style.RESET_ALL}")
    print(f"{Fore.RED}Error: {error_msg}{Style.RESET_ALL}\n")
    
    if "Timestamp" in error_msg or "1021" in error_msg:
        print(f"{Fore.YELLOW}Timestamp Sync Issue Detected{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Solution:{Style.RESET_ALL}")
        print(f"  1. Sync your system clock")
        print(f"  2. Windows: Right-click taskbar clock → Adjust date/time → Sync now")
        print(f"  3. Or the bot will auto-adjust for timestamp differences\n")
    elif "API-key" in error_msg or "Invalid API" in error_msg:
        print(f"{Fore.YELLOW}API Key Issue Detected{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Solution:{Style.RESET_ALL}")
        print(f"  1. Verify API keys in .env file are correct")
        print(f"  2. Generate new keys from: https://testnet.binancefuture.com")
        print(f"  3. Make sure to copy the full key and secret\n")
    else:
        print(f"{Fore.YELLOW}Troubleshooting:{Style.RESET_ALL}")
        print(f"  1. Check your internet connection")
        print(f"  2. Verify testnet is accessible: https://testnet.binancefuture.com")
        print(f"  3. Check API key permissions (Futures trading enabled)")
        print(f"  4. Review bot.log for detailed error information\n")
