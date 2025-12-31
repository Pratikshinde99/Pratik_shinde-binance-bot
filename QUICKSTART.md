# Quick Start

Get the bot running in under 5 minutes.

## Step 1: Get API Keys

Head over to [Binance Futures Testnet](https://testnet.binancefuture.com), login with GitHub/Google, and generate your API keys.

## Step 2: Install

```bash
pip install -r requirements.txt
```

## Step 3: Configure

```bash
cp .env.example .env
```

Edit `.env` and paste your API credentials:
```
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here
TESTNET=True
```

## Step 4: Run

```bash
cd src
python main.py
```

## First Trade

Try a small market order:
```bash
python market_orders.py BTCUSDT BUY 0.002
```

Remember: Minimum order value is $100, so 0.002 BTC works at current prices.

## Common Issues

**"Module not found"** → Run `pip install -r requirements.txt`

**"API credentials not found"** → Check your `.env` file exists and has correct keys

**"Notional must be no smaller than 100"** → Increase quantity (min $100 order value)

**Timestamp errors** → The bot auto-syncs, but you can manually sync your system clock if needed

## What's Next?

- Check out the different order types in the interactive menu
- Read the full README for detailed documentation
- Try the advanced strategies in the `advanced/` folder

Questions? Email me at ps175581@gmail.com
