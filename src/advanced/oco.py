"""
OCO (One-Cancels-the-Other) Order implementation for Binance Futures
Places take-profit and stop-loss orders simultaneously
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from binance.exceptions import BinanceAPIException
from base_bot import BasicBot
from logger import logger
from validator import Validator, ValidationError
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class OCOBot(BasicBot):
    """Bot for executing OCO (One-Cancels-the-Other) orders"""
    
    def place_oco_order(self, symbol, side, quantity, take_profit_price, stop_loss_price):
        """
        Place an OCO order (simulated with two separate orders)
        
        Note: Binance Futures doesn't have native OCO support, so we simulate it
        by placing a take-profit limit order and a stop-loss market order
        
        Args:
            symbol: Trading pair (e.g., BTCUSDT)
            side: BUY or SELL (for closing position)
            quantity: Order quantity
            take_profit_price: Take profit limit price
            stop_loss_price: Stop loss trigger price
            
        Returns:
            Dict with both order responses
        """
        try:
            # Validate inputs
            symbol = Validator.validate_symbol(symbol)
            side = Validator.validate_side(side)
            quantity = Validator.validate_quantity(quantity)
            take_profit_price = Validator.validate_price(take_profit_price)
            stop_loss_price = Validator.validate_price(stop_loss_price)
            
            # Get current price for reference
            current_price = self.get_current_price(symbol)
            logger.info(f"Current market price: {current_price}")
            
            # Validate price logic
            if side == 'SELL':
                if take_profit_price <= current_price:
                    raise ValidationError(
                        f"For SELL, take profit ({take_profit_price}) must be above current price ({current_price})"
                    )
                if stop_loss_price >= current_price:
                    raise ValidationError(
                        f"For SELL, stop loss ({stop_loss_price}) must be below current price ({current_price})"
                    )
            
            logger.log_order('OCO', symbol, side, quantity, take_profit_price)
            
            # Place Take Profit Order
            tp_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='TAKE_PROFIT_MARKET',
                quantity=quantity,
                stopPrice=take_profit_price
            )
            
            logger.info(f"Take profit order placed: {tp_order['orderId']}")
            
            # Place Stop Loss Order
            sl_order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type='STOP_MARKET',
                quantity=quantity,
                stopPrice=stop_loss_price
            )
            
            logger.info(f"Stop loss order placed: {sl_order['orderId']}")
            
            print(f"\n{Fore.GREEN}✓ OCO Orders Placed Successfully!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}Take Profit Order:{Style.RESET_ALL}")
            print(f"  Order ID: {tp_order['orderId']}")
            print(f"  Stop Price: {tp_order['stopPrice']}")
            
            print(f"\n{Fore.CYAN}Stop Loss Order:{Style.RESET_ALL}")
            print(f"  Order ID: {sl_order['orderId']}")
            print(f"  Stop Price: {sl_order['stopPrice']}")
            
            return {
                'take_profit_order': tp_order,
                'stop_loss_order': sl_order
            }
            
        except ValidationError as e:
            logger.error(f"Validation error: {e}")
            print(f"\n{Fore.RED}✗ Validation Error:{Style.RESET_ALL} {e}")
            raise
        except Exception as e:
            logger.log_error_trace(e, "Error placing OCO order")
            print(f"\n{Fore.RED}✗ Error:{Style.RESET_ALL} {str(e)}")
            raise

def main():
    """CLI entry point for OCO orders"""
    print(f"\n{Fore.YELLOW}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}Binance Futures - OCO Order Bot{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}{'='*60}{Style.RESET_ALL}\n")
    
    if len(sys.argv) < 6:
        print(f"{Fore.RED}Usage:{Style.RESET_ALL} python oco.py <SYMBOL> <SIDE> <QUANTITY> <TAKE_PROFIT> <STOP_LOSS>")
        print(f"\n{Fore.CYAN}Example:{Style.RESET_ALL} python oco.py BTCUSDT SELL 0.01 52000 48000")
        sys.exit(1)
    
    symbol = sys.argv[1]
    side = sys.argv[2]
    quantity = sys.argv[3]
    take_profit_price = sys.argv[4]
    stop_loss_price = sys.argv[5]
    
    try:
        bot = OCOBot(testnet=True)
        balance = bot.get_account_balance()
        print(f"\n{Fore.GREEN}Account Balance:{Style.RESET_ALL} {balance['total_balance']} USDT\n")
        
        orders = bot.place_oco_order(
            symbol, side, float(quantity),
            float(take_profit_price), float(stop_loss_price)
        )
        
        print(f"\n{Fore.GREEN}OCO orders placed successfully!{Style.RESET_ALL}\n")
        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Operation cancelled{Style.RESET_ALL}")
        sys.exit(0)
    except Exception:
        sys.exit(1)

if __name__ == "__main__":
    main()
