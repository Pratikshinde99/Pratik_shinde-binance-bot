# Project Notes

Just some personal notes on the project structure and what I built.

## What This Is

A trading bot for Binance Futures that I built to learn about algorithmic trading. Supports different order types and some automated strategies.

## File Organization

```
Binance/
├── src/
│   ├── market_orders.py
│   ├── limit_orders.py
│   ├── base_bot.py
│   ├── config.py
│   ├── logger.py
│   ├── validator.py
│   ├── main.py
│   └── advanced/
│       ├── stop_limit.py
│       ├── oco.py
│       ├── twap.py
│       └── grid_strategy.py
├── requirements.txt
├── .env.example
└── README.md
```

## Order Types Implemented

**Basic:**
- Market orders - instant execution
- Limit orders - set your price

**Advanced:**
- Stop-limit - triggered orders
- OCO - take profit + stop loss combo
- TWAP - split orders over time
- Grid - range trading automation

## Tech Stack

- Python 3.11
- python-binance library
- Binance Futures Testnet API
- colorama for terminal colors

## Features

- Input validation before API calls
- Comprehensive logging to file
- Colored CLI output
- Interactive menu interface
- Error handling with clear messages
- Automatic timestamp sync

## Stats

- ~2,500 lines of code
- 13 Python files
- 6 order types
- 100% testnet (no real money)

## Things I Learned

- How futures trading APIs work
- Importance of validation in financial systems
- Timestamp synchronization
- Error handling patterns
- Logging best practices

## Known Issues

- OCO orders need manual cancellation of unfilled order (Futures API limitation)
- Minimum $100 order size (Binance requirement)
- Need to sync system clock if timestamp errors occur

## Testing

Everything tested on Binance Futures Testnet. Started with small orders to verify functionality.

## Contact

ps175581@gmail.com for questions or collaboration

## License

MIT - use it however you want
