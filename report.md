# Binance Futures Trading Bot - Project Report

**Author:** Pratik Shinde  
**Email:** ps175581@gmail.com  
**GitHub:** https://github.com/Pratikshinde99/Pratik_shinde-binance-bot  
**Date:** December 31, 2025

---

## Project Overview

This project implements an automated trading bot for Binance USDT-M Futures with support for multiple order types and trading strategies. Built using Python and the Binance API, it provides both basic and advanced order execution capabilities through a command-line interface.

---

## Implementation

### Core Order Types

#### 1. Market Orders (`src/market_orders.py`)
Executes trades immediately at the current market price. This is useful when quick execution is more important than getting a specific price.

**Features:**
- Instant execution at best available price
- Real-time price display
- Order confirmation with execution details
- Comprehensive error handling

**Usage:**
```bash
python market_orders.py BTCUSDT BUY 0.002
```

#### 2. Limit Orders (`src/limit_orders.py`)
Places orders at specific price levels with configurable time-in-force options.

**Features:**
- Set custom entry/exit prices
- Time-in-force options: GTC, IOC, FOK
- Price difference calculation
- Order status tracking

**Usage:**
```bash
python limit_orders.py BTCUSDT BUY 0.002 85000 GTC
```

---

### Advanced Order Types

#### 3. Stop-Limit Orders (`src/advanced/stop_limit.py`)
Triggers a limit order when price reaches a specified stop level.

**Use Cases:**
- Stop-loss protection on existing positions
- Breakout entries when price crosses resistance levels
- Automated risk management

**Implementation:**
The bot validates that stop prices make sense (e.g., for SELL orders, stop must be below current price).

**Usage:**
```bash
python stop_limit.py BTCUSDT SELL 0.002 87000 86500
```

#### 4. OCO Orders (`src/advanced/oco.py`)
Places both take-profit and stop-loss orders simultaneously. When one executes, the other should be cancelled.

**Features:**
- Automated profit-taking
- Risk management
- Position protection

**Note:** Since Binance Futures doesn't support native OCO, I implemented it using separate TAKE_PROFIT_MARKET and STOP_MARKET orders.

**Usage:**
```bash
python oco.py BTCUSDT SELL 0.002 92000 85000
```

#### 5. TWAP Strategy (`src/advanced/twap.py`)
Time-Weighted Average Price execution splits large orders into smaller chunks over time.

**Benefits:**
- Reduces market impact
- Better average execution price
- Configurable intervals and order count

**Usage:**
```bash
python twap.py BTCUSDT BUY 0.01 5 60
```

#### 6. Grid Trading (`src/advanced/grid_strategy.py`)
Automatically places buy and sell orders at multiple price levels within a specified range.

**Strategy:**
- Places buy orders below current price
- Places sell orders above current price
- Profits from price oscillation in range

**Usage:**
```bash
python grid_strategy.py BTCUSDT 85000 90000 10 0.001
```

---

## System Architecture

### Core Components

**1. Base Bot (`src/base_bot.py`)**
- Handles API connection and authentication
- Provides common functions for all order types
- Manages timestamp synchronization
- Account and position management

**2. Configuration (`src/config.py`)**
- Centralized settings management
- Environment variable loading
- API credential handling
- Trading parameters

**3. Logger (`src/logger.py`)**
- Structured logging to file and console
- Timestamps on all operations
- Error traces with full stack information
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)

**4. Validator (`src/validator.py`)**
- Input validation before API calls
- Symbol format checking
- Quantity and price validation
- Order type verification

**5. Interactive Menu (`src/main.py`)**
- User-friendly CLI interface
- Access to all order types
- Account information display
- Position and order management

---

## Technical Challenges & Solutions

### Challenge 1: Timestamp Synchronization
**Problem:** Binance API requires request timestamps within 1000ms of server time.

**Solution:** Implemented automatic timestamp offset calculation in the base bot. The bot fetches server time and calculates the difference with local time, then applies this offset to all requests.

```python
server_time = self.client.get_server_time()
local_time = int(time.time() * 1000)
time_offset = server_time['serverTime'] - local_time
self.client.timestamp_offset = time_offset
```

### Challenge 2: Minimum Order Size
**Problem:** Binance enforces a $100 minimum notional value per order.

**Solution:** Added validation and clear error messages. The bot calculates notional value (quantity × price) and provides helpful feedback when orders are too small.

### Challenge 3: OCO Implementation
**Problem:** Binance Futures API doesn't support native OCO orders like the spot market.

**Solution:** Simulated OCO by placing separate TAKE_PROFIT_MARKET and STOP_MARKET orders. Users need to manually cancel the unfilled order when one executes.

### Challenge 4: Error Handling
**Problem:** Need to handle various API errors gracefully.

**Solution:** Implemented comprehensive try-catch blocks with specific error handling for:
- Validation errors
- API exceptions
- Network issues
- Timestamp errors

---

## Testing & Validation

All testing was conducted on Binance Futures Testnet to ensure safety.

### Test Results

| Order Type | Test Scenario | Result | Notes |
|------------|---------------|--------|-------|
| Market | Buy 0.002 BTC | ✅ Pass | Executed instantly |
| Market | Sell 0.03 ETH | ✅ Pass | Proper validation |
| Limit | Buy at specific price | ✅ Pass | Order placed correctly |
| Limit | Different TIF options | ✅ Pass | GTC, IOC, FOK all work |
| Stop-Limit | Sell with stop | ✅ Pass | Validation working |
| OCO | TP + SL combo | ✅ Pass | Both orders placed |
| TWAP | 5 orders over 1 min | ✅ Pass | Proper timing |
| Grid | 10-level grid | ✅ Pass | All orders placed |

### Validation Testing
- ✅ Invalid symbols rejected
- ✅ Negative quantities rejected
- ✅ Invalid prices rejected
- ✅ Minimum order size enforced
- ✅ Proper error messages displayed

---

## Key Learnings

### Technical Skills
- Working with financial APIs and handling rate limits
- Timestamp synchronization in distributed systems
- Order validation and risk management
- Structured logging for debugging
- Error handling in production systems

### Trading Concepts
- Different order types and their use cases
- Market impact and TWAP execution
- Grid trading in range-bound markets
- Risk management with OCO orders
- Futures trading mechanics

### Software Engineering
- Modular code architecture
- Separation of concerns
- Input validation importance
- Comprehensive error handling
- Documentation best practices

---

## Code Quality

### Design Principles
- **Modularity:** Each order type in separate file
- **Reusability:** Common functions in base bot
- **Validation:** All inputs checked before API calls
- **Logging:** Comprehensive audit trail
- **Error Handling:** Graceful failure with clear messages

### Code Statistics
- Total Lines: ~2,500+
- Python Files: 13
- Order Types: 6
- Functions: 50+
- Classes: 7

---

## Future Enhancements

Potential improvements for future development:

1. **WebSocket Integration**
   - Real-time price updates
   - Order fill notifications
   - Reduced API calls

2. **Position Management**
   - Automatic position sizing
   - Risk calculation based on account balance
   - Portfolio tracking

3. **Backtesting Framework**
   - Historical data analysis
   - Strategy performance metrics
   - Optimization tools

4. **Web Dashboard**
   - Visual monitoring interface
   - Real-time charts
   - Order management UI

5. **Additional Strategies**
   - DCA (Dollar Cost Averaging)
   - Trailing stops
   - Momentum-based entries

---

## Dependencies

- **python-binance (1.0.19)** - Official Binance API wrapper
- **colorama (0.4.6)** - Terminal color output
- **python-dotenv (1.0.0)** - Environment variable management
- **requests (2.31.0)** - HTTP library
- **tabulate (0.9.0)** - Table formatting

---

## Security Considerations

- API keys stored in `.env` file (not committed to Git)
- `.gitignore` prevents accidental credential exposure
- Testnet-first approach for safe development
- Input validation prevents injection attacks
- Comprehensive logging for audit trails

---

## Conclusion

This project successfully implements a comprehensive trading bot for Binance Futures with multiple order types and strategies. The modular architecture makes it easy to add new features or modify existing ones.

Key achievements:
- ✅ All required order types implemented
- ✅ Advanced strategies working correctly
- ✅ Robust error handling and validation
- ✅ Comprehensive logging system
- ✅ Clean, maintainable code
- ✅ Complete documentation

The bot provides a solid foundation for algorithmic trading experimentation and can be extended with additional strategies and features.

---

## Repository

**GitHub:** https://github.com/Pratikshinde99/Pratik_shinde-binance-bot

---

## Contact

**Pratik Shinde**  
Email: ps175581@gmail.com  
GitHub: [@Pratikshinde99](https://github.com/Pratikshinde99)

---

## Disclaimer

This is an educational project developed for learning purposes. Cryptocurrency trading involves significant risk. Always test thoroughly on testnet before considering any live trading. Never invest more than you can afford to lose.

---

**End of Report**
