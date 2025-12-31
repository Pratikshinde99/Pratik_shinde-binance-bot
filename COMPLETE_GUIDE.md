# Complete Guide

Everything you need to know about using this trading bot.

## What It Does

This bot connects to Binance Futures Testnet and lets you place different types of orders through a command-line interface. I built it to learn about algorithmic trading and practice working with financial APIs.

## Setup

### Get API Keys
1. Go to https://testnet.binancefuture.com
2. Login with GitHub or Google
3. Generate API keys
4. Save them somewhere safe

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure
Create a `.env` file:
```bash
cp .env.example .env
```

Add your keys:
```
BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret
TESTNET=True
```

## Using the Bot

### Interactive Mode
```bash
cd src
python main.py
```

This gives you a menu with all the options.

### Direct Commands

**Market Order** (instant execution):
```bash
python market_orders.py BTCUSDT BUY 0.002
```

**Limit Order** (set your price):
```bash
python limit_orders.py BTCUSDT BUY 0.002 85000
```

**Stop-Limit** (triggered order):
```bash
cd advanced
python stop_limit.py BTCUSDT SELL 0.002 87000 86500
```

**OCO** (take profit + stop loss):
```bash
python oco.py BTCUSDT SELL 0.002 92000 85000
```

**TWAP** (split order over time):
```bash
python twap.py BTCUSDT BUY 0.01 5 60
```

**Grid Trading** (range automation):
```bash
python grid_strategy.py BTCUSDT 85000 90000 10 0.001
```

## Order Types Explained

### Market Orders
Executes immediately at current price. Use when you want to get in/out fast and don't care about the exact price.

### Limit Orders
Only executes at your specified price or better. Good for planned entries when you're not in a rush.

### Stop-Limit
Triggers a limit order when price hits your stop level. I use this for:
- Stop losses on positions
- Buying breakouts above resistance

### OCO (One-Cancels-Other)
Places both a take-profit and stop-loss. When one fills, the other cancels automatically. Great for managing positions while you're away.

### TWAP
Splits a large order into smaller pieces over time. Helps reduce market impact and get better average prices.

### Grid Trading
Places multiple buy/sell orders at different price levels. Works well when price is ranging between support and resistance.

## Important Stuff

### Minimum Order Size
Binance requires $100 minimum per order. So:
- BTC at $88k: need at least 0.0012 BTC
- ETH at $3.3k: need at least 0.031 ETH

### Testnet Money
The testnet gives you fake USDT to practice with. It's not real money, so feel free to experiment.

### Logs
Everything gets logged to `bot.log`. Check it if something goes wrong.

## Common Issues

**"Module not found"**
→ Run `pip install -r requirements.txt`

**"API credentials not found"**
→ Make sure `.env` file exists with your keys

**"Notional must be no smaller than 100"**
→ Increase your order size (minimum $100)

**Timestamp errors**
→ The bot auto-syncs, but sync your system clock if it persists

## Architecture

The code is organized into modules:
- `base_bot.py` - Core API stuff
- `config.py` - Settings and credentials
- `logger.py` - Logging system
- `validator.py` - Input checking
- Individual files for each order type

Each order type extends the base bot and adds its specific logic.

## Testing

I tested everything on testnet with small orders first. Recommend you do the same before trying anything larger.

## Future Ideas

Some things I might add:
- WebSocket for real-time prices
- Backtesting framework
- Web interface
- More strategies

## Tech Details

Built with:
- Python 3.11
- python-binance library
- Binance Futures API
- colorama for colors

## Questions?

Email me: ps175581@gmail.com

## Disclaimer

This is a learning project. Trading crypto is risky. Only use testnet until you really know what you're doing.
