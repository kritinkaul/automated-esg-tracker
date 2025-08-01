#!/usr/bin/env python3
"""
Test script to verify data accuracy improvements
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ultimate_dashboard import get_stock_data, generate_sample_stock_data, get_financial_metrics

def test_stock_data():
    """Test stock data accuracy"""
    print("🧪 Testing Stock Data Accuracy")
    print("=" * 50)
    
    test_symbols = ["MSFT", "AAPL", "GOOGL", "TSLA"]
    
    for symbol in test_symbols:
        print(f"\nTesting {symbol}:")
        
        # Test real data first
        real_data = get_stock_data(symbol)
        if real_data is not None and not real_data.empty:
            current_price = real_data['Close'].iloc[-1]
            print(f"  ✅ Real data: ${current_price:.2f}")
        else:
            print(f"  ⚠️  Real data unavailable, testing fallback...")
            
            # Test fallback data
            sample_data = generate_sample_stock_data(symbol)
            if sample_data is not None and not sample_data.empty:
                current_price = sample_data['Close'].iloc[-1]
                print(f"  📊 Sample data: ${current_price:.2f}")
                
                # Verify realistic price ranges
                if symbol == "MSFT" and 350 <= current_price <= 480:
                    print(f"  ✅ MSFT price range looks realistic")
                elif symbol == "AAPL" and 150 <= current_price <= 220:
                    print(f"  ✅ AAPL price range looks realistic")
                elif symbol == "GOOGL" and 100 <= current_price <= 180:
                    print(f"  ✅ GOOGL price range looks realistic")
                elif symbol == "TSLA" and 180 <= current_price <= 300:
                    print(f"  ✅ TSLA price range looks realistic")
                else:
                    print(f"  ❌ Price ${current_price:.2f} seems unrealistic for {symbol}")
            else:
                print(f"  ❌ Sample data generation failed")

def test_financial_metrics():
    """Test financial metrics accuracy"""
    print("\n\n💰 Testing Financial Metrics")
    print("=" * 50)
    
    test_symbols = ["MSFT", "AAPL", "GOOGL", "TSLA"]
    
    for symbol in test_symbols:
        print(f"\nTesting {symbol} financial metrics:")
        
        metrics = get_financial_metrics(symbol)
        if metrics:
            current_price = metrics.get('current_price', 0)
            market_cap = metrics.get('market_cap', 0)
            pe_ratio = metrics.get('pe_ratio', 0)
            
            print(f"  Current Price: ${current_price:.2f}")
            print(f"  Market Cap: ${market_cap/1e9:.1f}B")
            print(f"  P/E Ratio: {pe_ratio:.1f}")
            
            # Basic validation
            if current_price > 0:
                print(f"  ✅ Price data looks valid")
            else:
                print(f"  ❌ Invalid price data")
                
            if market_cap > 0:
                print(f"  ✅ Market cap data looks valid")
            else:
                print(f"  ❌ Invalid market cap data")
        else:
            print(f"  ❌ No financial metrics available")

if __name__ == "__main__":
    print("🚀 Starting Data Accuracy Tests\n")
    
    test_stock_data()
    test_financial_metrics()
    
    print("\n\n✅ Testing Complete!")
    print("\nNow check the Streamlit dashboard at http://localhost:8501")
    print("Look for MSFT price around $415 instead of $131!") 