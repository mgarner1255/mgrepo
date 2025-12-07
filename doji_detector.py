#!/usr/bin/env python3
"""
Doji Pattern Detector for Stock Trading

This script identifies doji candlestick patterns from stock price data.
A doji is a candlestick pattern where the open and close prices are nearly equal,
indicating market indecision.

Types of Doji patterns detected:
- Standard Doji: Open and close are nearly equal
- Long-legged Doji: Open and close are nearly equal with long upper and lower shadows
- Dragonfly Doji: Open and close are at the high of the period
- Gravestone Doji: Open and close are at the low of the period
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Candle:
    """Represents a single candlestick with OHLCV data"""
    timestamp: str
    open: float
    high: float
    low: float
    close: float
    volume: float


class DojiDetector:
    """
    Detects doji candlestick patterns in stock price data
    """

    def __init__(self, doji_threshold: float = 0.1):
        """
        Initialize the DojiDetector

        Args:
            doji_threshold: Maximum ratio of body to total range to be considered a doji (default: 0.1 or 10%)
        """
        self.doji_threshold = doji_threshold
        self.detected_patterns = []

    def calculate_body_size(self, candle: Candle) -> float:
        """Calculate the absolute size of the candle body"""
        return abs(candle.close - candle.open)

    def calculate_total_range(self, candle: Candle) -> float:
        """Calculate the total range (high to low) of the candle"""
        return candle.high - candle.low

    def calculate_upper_shadow(self, candle: Candle) -> float:
        """Calculate the upper shadow (wick) length"""
        return candle.high - max(candle.open, candle.close)

    def calculate_lower_shadow(self, candle: Candle) -> float:
        """Calculate the lower shadow (tail) length"""
        return min(candle.open, candle.close) - candle.low

    def is_doji(self, candle: Candle) -> bool:
        """
        Determine if a candle is a doji pattern

        A doji is identified when the body is very small relative to the total range
        """
        total_range = self.calculate_total_range(candle)

        # Avoid division by zero for candles with no range
        if total_range == 0:
            return True

        body_size = self.calculate_body_size(candle)
        body_ratio = body_size / total_range

        return body_ratio <= self.doji_threshold

    def identify_doji_type(self, candle: Candle) -> Optional[str]:
        """
        Identify the specific type of doji pattern

        Returns:
            String describing the doji type, or None if not a doji
        """
        if not self.is_doji(candle):
            return None

        total_range = self.calculate_total_range(candle)

        # Handle case where there's no price movement
        if total_range == 0:
            return "Perfect Doji (No Price Movement)"

        upper_shadow = self.calculate_upper_shadow(candle)
        lower_shadow = self.calculate_lower_shadow(candle)
        body_midpoint = (candle.open + candle.close) / 2
        range_midpoint = (candle.high + candle.low) / 2

        # Dragonfly Doji: Open/close near the high, long lower shadow
        if upper_shadow / total_range < 0.1 and lower_shadow / total_range > 0.6:
            return "Dragonfly Doji"

        # Gravestone Doji: Open/close near the low, long upper shadow
        if lower_shadow / total_range < 0.1 and upper_shadow / total_range > 0.6:
            return "Gravestone Doji"

        # Long-legged Doji: Both shadows are significant
        if (upper_shadow / total_range > 0.3 and lower_shadow / total_range > 0.3):
            return "Long-legged Doji"

        # Standard Doji: Default case
        return "Standard Doji"

    def analyze_candle(self, candle: Candle) -> Optional[Dict]:
        """
        Analyze a single candle for doji patterns

        Returns:
            Dictionary with pattern details if doji found, None otherwise
        """
        doji_type = self.identify_doji_type(candle)

        if doji_type:
            pattern_info = {
                'timestamp': candle.timestamp,
                'type': doji_type,
                'open': candle.open,
                'high': candle.high,
                'low': candle.low,
                'close': candle.close,
                'volume': candle.volume,
                'body_size': self.calculate_body_size(candle),
                'total_range': self.calculate_total_range(candle),
                'upper_shadow': self.calculate_upper_shadow(candle),
                'lower_shadow': self.calculate_lower_shadow(candle)
            }
            return pattern_info

        return None

    def scan_candles(self, candles: List[Candle]) -> List[Dict]:
        """
        Scan a list of candles for doji patterns

        Args:
            candles: List of Candle objects to analyze

        Returns:
            List of detected patterns with details
        """
        self.detected_patterns = []

        for candle in candles:
            pattern = self.analyze_candle(candle)
            if pattern:
                self.detected_patterns.append(pattern)

        return self.detected_patterns

    def print_patterns(self):
        """Print detected patterns in a formatted way"""
        if not self.detected_patterns:
            print("No doji patterns detected.")
            return

        print(f"\n{'='*80}")
        print(f"DOJI PATTERNS DETECTED: {len(self.detected_patterns)}")
        print(f"{'='*80}\n")

        for i, pattern in enumerate(self.detected_patterns, 1):
            print(f"Pattern #{i}: {pattern['type']}")
            print(f"  Timestamp: {pattern['timestamp']}")
            print(f"  Open:      ${pattern['open']:.2f}")
            print(f"  High:      ${pattern['high']:.2f}")
            print(f"  Low:       ${pattern['low']:.2f}")
            print(f"  Close:     ${pattern['close']:.2f}")
            print(f"  Volume:    {pattern['volume']:,.0f}")
            print(f"  Body Size: ${pattern['body_size']:.2f}")
            print(f"  Range:     ${pattern['total_range']:.2f}")
            print(f"  Upper Shadow: ${pattern['upper_shadow']:.2f}")
            print(f"  Lower Shadow: ${pattern['lower_shadow']:.2f}")
            print(f"{'-'*80}")


def main():
    """Example usage of the DojiDetector"""

    # Example stock data (timestamp, open, high, low, close, volume)
    sample_data = [
        Candle("2025-01-01 09:30", 150.00, 152.00, 148.00, 150.50, 1000000),  # Standard Doji
        Candle("2025-01-01 10:00", 151.00, 155.00, 150.00, 154.00, 1200000),  # Not a doji
        Candle("2025-01-01 10:30", 154.50, 154.80, 151.00, 154.70, 900000),   # Dragonfly Doji
        Candle("2025-01-01 11:00", 155.00, 158.00, 154.50, 155.20, 1100000),  # Gravestone Doji
        Candle("2025-01-01 11:30", 155.50, 157.50, 153.00, 155.40, 1300000),  # Long-legged Doji
        Candle("2025-01-01 12:00", 156.00, 158.00, 155.00, 157.50, 1050000),  # Not a doji
    ]

    # Create detector with 10% threshold (body must be <= 10% of total range)
    detector = DojiDetector(doji_threshold=0.1)

    # Scan for patterns
    print("Scanning candles for doji patterns...")
    patterns = detector.scan_candles(sample_data)

    # Display results
    detector.print_patterns()

    # Additional analysis
    if patterns:
        print(f"\nSummary:")
        print(f"  Total candles analyzed: {len(sample_data)}")
        print(f"  Doji patterns found: {len(patterns)}")
        print(f"  Detection rate: {len(patterns)/len(sample_data)*100:.1f}%")

        # Count pattern types
        pattern_types = {}
        for pattern in patterns:
            ptype = pattern['type']
            pattern_types[ptype] = pattern_types.get(ptype, 0) + 1

        print(f"\nPattern Type Distribution:")
        for ptype, count in pattern_types.items():
            print(f"  {ptype}: {count}")


if __name__ == "__main__":
    main()
