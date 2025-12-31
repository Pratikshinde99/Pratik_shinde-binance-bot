# Binance Futures Trading Bot - Technical Report

**Author:** Prashant Sharma  
**Email:** ps175581@gmail.com  
**Date:** December 2025  
**Project:** Automated Trading Bot for Binance USDT-M Futures

---

## Overview

This project implements a command-line trading bot for Binance Futures with support for multiple order types and automated trading strategies. The bot was developed to explore algorithmic trading concepts and practice working with financial APIs.

---

## Implementation

### Core Order Types

#### Market Orders
Implemented in `src/market_orders.py`. Executes trades immediately at the best available price. Useful for quick entries/exits when price is more important than timing.

#### Limit Orders
Implemented in `src/limit_orders.py`. Places orders at specific price levels with configurable time-in-force options (GTC, IOC, FOK). Better for planned entries at desired prices.

### Advanced Strategies

#### Stop-Limit Orders
File: `src/advanced/stop_limit.py`

Triggers a limit order when price reaches a stop level. I use this for:
- Stop-loss protection on existing positions
- Breakout entries when price crosses resistance

#### OCO (One-Cancels-Other)
File: `src/advanced/oco.py`

Places both take-profit and stop-loss orders simultaneously. When one executes, the other is cancelled. Great for automated risk management.

Note: Binance Futures doesn't have native OCO support, so I implemented it using separate TAKE_PROFIT_MARKET and STOP_MARKET orders.

#### TWAP (Time-Weighted Average Price)
File: `src/advanced/twap.py`

Splits large orders into smaller chunks executed over time. This reduces market impact and helps get better average prices on bigger positions.

#### Grid Trading
File: `src/advanced/grid_strategy.py`

Automatically places buy and sell orders at multiple price levels within a range. Works well in sideways markets where price oscillates within a known range.

### System Architecture

The bot is built with a modular structure:

- `base_bot.py` - Core API communication and common functions
- `config.py` - Centralized configuration and environment variables
- `logger.py` - Structured logging with file and console output
- `validator.py` - Input validation before API calls

Each order type extends the base bot functionality and adds specific logic.

---

## Technical Challenges

### Timestamp Synchronization
Binance API requires timestamps within 1000ms of server time. I added automatic timestamp offset calculation in the base bot to handle this.

### Minimum Order Size
Binance enforces a $100 minimum notional value per order. Had to add validation and clear error messages for this.

### OCO Implementation
Since Futures API doesn't support native OCO, I simulated it with separate orders. Users need to manually cancel the unfilled order when one executes.

---

## Testing

All testing was done on Binance Futures Testnet. Tested scenarios:
- Market orders (buy/sell)
- Limit orders with different TIF options
- Stop-limit triggers
- OCO order placement
- TWAP execution over various intervals
- Grid setup with different price ranges

---

## Key Learnings

- Working with financial APIs and handling rate limits
- Importance of proper error handling in trading systems
- Timestamp synchronization in distributed systems
- Order validation and risk management
- Logging for debugging and audit trails

---

## Future Improvements

Some ideas for future development:
- WebSocket integration for real-time price updates
- Position sizing based on account balance
- Backtesting framework for strategies
- Web dashboard for monitoring
- More advanced strategies (DCA, trailing stops, etc.)

---

## Code Quality

- Modular design with separation of concerns
- Comprehensive input validation
- Detailed logging for all operations
- Error handling with informative messages
- Documentation and code comments

---

## Dependencies

- `python-binance` - Official Binance API wrapper
- `colorama` - Terminal color output
- `python-dotenv` - Environment variable management
- `requests` - HTTP library

---

## Conclusion

This project gave me hands-on experience with algorithmic trading concepts and API integration. The bot successfully implements multiple order types and strategies while maintaining clean, maintainable code.

The modular architecture makes it easy to add new strategies or modify existing ones. All core functionality works as expected on testnet.

---

## Repository

Code available at: [Add your GitHub link]

## Contact

Prashant Sharma  
Email: ps175581@gmail.com

---

*Note: This is an educational project. Always test thoroughly and understand the risks before any live trading.*
