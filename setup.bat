@echo off
REM Binance Futures Trading Bot - Setup Script
REM This script helps you set up the bot quickly

echo.
echo ========================================
echo Binance Futures Trading Bot - Setup
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [OK] Python is installed
python --version
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo [OK] pip is available
echo.

REM Install dependencies
echo Installing dependencies...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [OK] Dependencies installed successfully
echo.

REM Check if .env file exists
if exist .env (
    echo [OK] .env file already exists
) else (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo [OK] .env file created
    echo.
    echo ========================================
    echo IMPORTANT: Configure your API keys
    echo ========================================
    echo.
    echo Please edit the .env file and add your Binance Testnet API credentials:
    echo 1. Open .env file in a text editor
    echo 2. Replace 'your_testnet_api_key_here' with your actual API key
    echo 3. Replace 'your_testnet_api_secret_here' with your actual API secret
    echo.
    echo Get your API keys from: https://testnet.binancefuture.com
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Configure your API keys in .env file
echo 2. Run the bot: cd src ^&^& python main.py
echo 3. Or try a quick test: cd src ^&^& python market_orders.py BTCUSDT BUY 0.001
echo.
echo For detailed instructions, see:
echo - QUICKSTART.md (5-minute guide)
echo - README.md (full documentation)
echo.

pause
