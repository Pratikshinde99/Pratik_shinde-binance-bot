#!/bin/bash
# Binance Futures Trading Bot - Setup Script (Linux/Mac)
# This script helps you set up the bot quickly

echo ""
echo "========================================"
echo "Binance Futures Trading Bot - Setup"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "[OK] Python is installed"
python3 --version
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] pip3 is not available"
    echo "Please ensure pip is installed with Python"
    exit 1
fi

echo "[OK] pip is available"
echo ""

# Install dependencies
echo "Installing dependencies..."
echo ""
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi

echo ""
echo "[OK] Dependencies installed successfully"
echo ""

# Check if .env file exists
if [ -f .env ]; then
    echo "[OK] .env file already exists"
else
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "[OK] .env file created"
    echo ""
    echo "========================================"
    echo "IMPORTANT: Configure your API keys"
    echo "========================================"
    echo ""
    echo "Please edit the .env file and add your Binance Testnet API credentials:"
    echo "1. Open .env file in a text editor"
    echo "2. Replace 'your_testnet_api_key_here' with your actual API key"
    echo "3. Replace 'your_testnet_api_secret_here' with your actual API secret"
    echo ""
    echo "Get your API keys from: https://testnet.binancefuture.com"
    echo ""
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "Next steps:"
echo "1. Configure your API keys in .env file"
echo "2. Run the bot: cd src && python3 main.py"
echo "3. Or try a quick test: cd src && python3 market_orders.py BTCUSDT BUY 0.001"
echo ""
echo "For detailed instructions, see:"
echo "- QUICKSTART.md (5-minute guide)"
echo "- README.md (full documentation)"
echo ""
