# Binance Futures Trading Bot

A Python-based automated trading bot for Binance USDT-M Futures. Built as part of my algorithmic trading project to explore different order execution strategies.

## Features

### Basic Order Types
- **Market Orders** - Quick execution at current prices
- **Limit Orders** - Set your own entry/exit prices

### Advanced Strategies
- **Stop-Limit Orders** - Automated stop-loss and breakout entries
- **OCO (One-Cancels-Other)** - Combined take-profit and stop-loss
- **TWAP** - Split large orders to reduce market impact
- **Grid Trading** - Range-bound automated trading

## Quick Setup

### Prerequisites
- Python 3.8+
- Binance Futures Testnet account

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/binance-futures-bot.git
cd binance-futures-bot

# Install dependencies
pip install -r requirements.txt

# Configure your API keys
cp .env.example .env
# Edit .env and add your Binance Testnet API credentials
```

### Get API Keys

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Login and generate API keys
3. Add them to your `.env` file

## Usage

### Interactive Menu
```bash
cd src
python main.py
```

### Direct Commands

**Market Order:**
```bash
python market_orders.py BTCUSDT BUY 0.002
```

**Limit Order:**
```bash
python limit_orders.py BTCUSDT BUY 0.002 85000
```

**Advanced Orders:**
```bash
cd advanced

# Stop-Limit
python stop_limit.py BTCUSDT SELL 0.002 87000 86500

# OCO
python oco.py BTCUSDT SELL 0.002 92000 85000

# TWAP
python twap.py BTCUSDT BUY 0.01 5 60

# Grid Trading
python grid_strategy.py BTCUSDT 85000 90000 10 0.001
```

## Project Structure

```
├── src/
│   ├── market_orders.py      # Market order execution
│   ├── limit_orders.py       # Limit order placement
│   ├── base_bot.py           # Core bot functionality
│   ├── config.py             # Configuration management
│   ├── logger.py             # Logging system
│   ├── validator.py          # Input validation
│   └── advanced/
│       ├── stop_limit.py     # Stop-limit orders
│       ├── oco.py            # OCO orders
│       ├── twap.py           # TWAP execution
│       └── grid_strategy.py  # Grid trading
├── requirements.txt
├── .env.example
└── README.md
```

## Important Notes

### Minimum Order Size
Binance requires minimum notional value of $100 per order:
- BTC: minimum ~0.0012 BTC (at $88k)
- ETH: minimum ~0.031 ETH (at $3.3k)

### Testnet vs Production
This bot is configured for testnet by default. Never use testnet API keys in production or vice versa.

## Logging

All trading activity is logged to `bot.log` with timestamps and detailed error information for debugging.

## Error Handling

The bot includes validation for:
- Symbol formats
- Order quantities
- Price values
- API responses

## Development

Built using:
- `python-binance` - Binance API wrapper
- `colorama` - Terminal colors
- `python-dotenv` - Environment management

## Disclaimer

This is an educational project. Cryptocurrency trading involves risk. Always test thoroughly on testnet before considering any live trading.

## Contact

For questions or issues: ps175581@gmail.com

## License

MIT License - feel free to use and modify for your own projects.
