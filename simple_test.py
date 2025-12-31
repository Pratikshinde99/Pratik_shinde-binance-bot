import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from binance.client import Client
from config import Config
import time

print("\n" + "="*60)
print("Simple API Connection Test")
print("="*60 + "\n")

try:
    print("1. Creating client...")
    client = Client(Config.API_KEY, Config.API_SECRET, testnet=True)
    
    print("2. Getting server time...")
    server_time_response = client.get_server_time()
    server_time = server_time_response['serverTime']
    local_time = int(time.time() * 1000)
    time_diff = server_time - local_time
    
    print(f"   Server time: {server_time}")
    print(f"   Local time:  {local_time}")
    print(f"   Difference:  {time_diff}ms")
    
    print("\n3. Setting timestamp offset...")
    client.timestamp_offset = time_diff
    print(f"   Offset set to: {time_diff}ms")
    
    print("\n4. Testing futures ping...")
    client.futures_ping()
    print("   ✓ Ping successful!")
    
    print("\n5. Getting account info...")
    account = client.futures_account()
    balance = float(account['totalWalletBalance'])
    print(f"   ✓ Account balance: {balance} USDT")
    
    print("\n" + "="*60)
    print("✓ ALL TESTS PASSED!")
    print("="*60 + "\n")
    
except Exception as e:
    print(f"\n✗ ERROR: {str(e)}\n")
    import traceback
    traceback.print_exc()
