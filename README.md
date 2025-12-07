# Doji Pattern Detector

An automated trading script in Python that identifies doji candlestick patterns from stock price data.

## Overview

This script analyzes stock price data (Open, High, Low, Close, Volume) and identifies various types of doji candlestick patterns, which are important indicators of market indecision in technical analysis.

## Doji Pattern Types Detected

1. **Standard Doji**: Open and close prices are nearly equal
2. **Dragonfly Doji**: Open/close near the high with a long lower shadow (bullish reversal signal)
3. **Gravestone Doji**: Open/close near the low with a long upper shadow (bearish reversal signal)
4. **Long-legged Doji**: Open/close near the middle with long upper and lower shadows (high volatility)

## Installation

No external dependencies required - uses only Python standard library.

```bash
python3 doji_detector.py
```

## Usage

### Basic Example

```python
from doji_detector import DojiDetector, Candle

# Create sample candle data
candles = [
    Candle("2025-01-01 09:30", 150.00, 152.00, 148.00, 150.50, 1000000),
    Candle("2025-01-01 10:00", 151.00, 155.00, 150.00, 154.00, 1200000),
]

# Initialize detector (default threshold: 5%)
detector = DojiDetector(doji_threshold=0.05)

# Scan for patterns
patterns = detector.scan_candles(candles)

# Display results
detector.print_patterns()
```

### Custom Integration

```python
from doji_detector import DojiDetector, Candle

# Create detector with custom threshold
detector = DojiDetector(doji_threshold=0.15)  # 15% body-to-range ratio

# Your stock data
candles = [
    Candle(timestamp, open_price, high_price, low_price, close_price, volume)
    for timestamp, open_price, high_price, low_price, close_price, volume in your_data
]

# Analyze
patterns = detector.scan_candles(candles)

# Access pattern details
for pattern in patterns:
    print(f"{pattern['timestamp']}: {pattern['type']}")
    print(f"  Price: ${pattern['close']:.2f}, Volume: {pattern['volume']:,}")
```

## Configuration

### Doji Threshold

The `doji_threshold` parameter controls how strict the doji detection is:

- **Lower values** (e.g., 0.03): Stricter detection, only very small bodies
- **Higher values** (e.g., 0.15): More lenient, detects doji with larger bodies
- **Default**: 0.05 (body must be ≤ 5% of total candle range)

## Output

The script provides detailed information for each detected pattern:

- Pattern type
- Timestamp
- OHLC prices (Open, High, Low, Close)
- Volume
- Body size
- Total range
- Upper and lower shadow lengths

## Running the Example

```bash
python3 doji_detector.py
```

This will run the built-in example with sample data and display detected patterns.

## Trading Interpretation

- **Dragonfly Doji**: Often signals bullish reversal after a downtrend
- **Gravestone Doji**: Often signals bearish reversal after an uptrend
- **Long-legged Doji**: Indicates high volatility and indecision
- **Standard Doji**: Shows equilibrium between buyers and sellers

**Note**: Always use doji patterns in conjunction with other technical indicators and never rely on a single signal for trading decisions.

## License

MIT