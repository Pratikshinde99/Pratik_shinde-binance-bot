"""
Input validation module for trading bot
Validates symbols, quantities, prices, and other trading parameters
"""
import re
from typing import Optional
from config import Config

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class Validator:
    """Validator class for trading parameters"""
    
    # Valid trading symbols pattern (e.g., BTCUSDT, ETHUSDT)
    SYMBOL_PATTERN = re.compile(r'^[A-Z]{2,10}USDT$')
    
    # Valid order sides
    VALID_SIDES = ['BUY', 'SELL']
    
    # Valid order types
    VALID_ORDER_TYPES = ['MARKET', 'LIMIT', 'STOP_MARKET', 'STOP_LIMIT', 'TAKE_PROFIT_MARKET']
    
    @staticmethod
    def validate_symbol(symbol: str) -> str:
        """
        Validate trading symbol
        
        Args:
            symbol: Trading pair symbol (e.g., BTCUSDT)
            
        Returns:
            Validated symbol in uppercase
            
        Raises:
            ValidationError: If symbol is invalid
        """
        if not symbol:
            raise ValidationError("Symbol cannot be empty")
        
        symbol = symbol.upper().strip()
        
        if not Validator.SYMBOL_PATTERN.match(symbol):
            raise ValidationError(
                f"Invalid symbol format: {symbol}. "
                "Expected format: BTCUSDT, ETHUSDT, etc."
            )
        
        return symbol
    
    @staticmethod
    def validate_side(side: str) -> str:
        """
        Validate order side
        
        Args:
            side: Order side (BUY or SELL)
            
        Returns:
            Validated side in uppercase
            
        Raises:
            ValidationError: If side is invalid
        """
        if not side:
            raise ValidationError("Side cannot be empty")
        
        side = side.upper().strip()
        
        if side not in Validator.VALID_SIDES:
            raise ValidationError(
                f"Invalid side: {side}. Must be BUY or SELL"
            )
        
        return side
    
    @staticmethod
    def validate_quantity(quantity: float, min_qty: Optional[float] = None) -> float:
        """
        Validate order quantity
        
        Args:
            quantity: Order quantity
            min_qty: Minimum quantity (optional)
            
        Returns:
            Validated quantity
            
        Raises:
            ValidationError: If quantity is invalid
        """
        try:
            quantity = float(quantity)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid quantity: {quantity}. Must be a number")
        
        if quantity <= 0:
            raise ValidationError(f"Quantity must be positive: {quantity}")
        
        min_check = min_qty if min_qty is not None else Config.MIN_QUANTITY
        if quantity < min_check:
            raise ValidationError(
                f"Quantity {quantity} is below minimum: {min_check}"
            )
        
        if quantity > Config.MAX_QUANTITY:
            raise ValidationError(
                f"Quantity {quantity} exceeds maximum: {Config.MAX_QUANTITY}"
            )
        
        return quantity
    
    @staticmethod
    def validate_price(price: float) -> float:
        """
        Validate order price
        
        Args:
            price: Order price
            
        Returns:
            Validated price
            
        Raises:
            ValidationError: If price is invalid
        """
        try:
            price = float(price)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid price: {price}. Must be a number")
        
        if price <= 0:
            raise ValidationError(f"Price must be positive: {price}")
        
        return price
    
    @staticmethod
    def validate_order_type(order_type: str) -> str:
        """
        Validate order type
        
        Args:
            order_type: Type of order
            
        Returns:
            Validated order type in uppercase
            
        Raises:
            ValidationError: If order type is invalid
        """
        if not order_type:
            raise ValidationError("Order type cannot be empty")
        
        order_type = order_type.upper().strip()
        
        if order_type not in Validator.VALID_ORDER_TYPES:
            raise ValidationError(
                f"Invalid order type: {order_type}. "
                f"Valid types: {', '.join(Validator.VALID_ORDER_TYPES)}"
            )
        
        return order_type
    
    @staticmethod
    def validate_leverage(leverage: int) -> int:
        """
        Validate leverage value
        
        Args:
            leverage: Leverage multiplier
            
        Returns:
            Validated leverage
            
        Raises:
            ValidationError: If leverage is invalid
        """
        try:
            leverage = int(leverage)
        except (ValueError, TypeError):
            raise ValidationError(f"Invalid leverage: {leverage}. Must be an integer")
        
        if leverage < 1 or leverage > Config.MAX_LEVERAGE:
            raise ValidationError(
                f"Leverage must be between 1 and {Config.MAX_LEVERAGE}"
            )
        
        return leverage
    
    @staticmethod
    def validate_time_in_force(time_in_force: str) -> str:
        """
        Validate time in force parameter
        
        Args:
            time_in_force: Time in force (GTC, IOC, FOK)
            
        Returns:
            Validated time in force
            
        Raises:
            ValidationError: If time in force is invalid
        """
        valid_tif = ['GTC', 'IOC', 'FOK']
        time_in_force = time_in_force.upper().strip()
        
        if time_in_force not in valid_tif:
            raise ValidationError(
                f"Invalid time in force: {time_in_force}. "
                f"Valid values: {', '.join(valid_tif)}"
            )
        
        return time_in_force
