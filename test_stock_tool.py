"""
Quick test script to verify stock price tool works
"""
import os
from dotenv import load_dotenv
from tools import StockPriceTool

# Load environment variables
load_dotenv()

# Test the stock tool
tool = StockPriceTool()

print("Testing Stock Price Tool (yfinance)...")
print("=" * 50)

# Test with NVDA
print("\n1. Testing NVDA (Nvidia):")
result = tool._run("NVDA")
print(result)

# Test with GOOGL
print("\n2. Testing GOOGL (Google):")
result = tool._run("GOOGL")
print(result)

print("\n" + "=" * 50)
print("✅ Stock tool is working!")
