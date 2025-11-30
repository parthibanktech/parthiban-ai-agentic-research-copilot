import os
from typing import Optional, Type
from langchain_core.tools import Tool, BaseTool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field


# --- Wikipedia Tool with Error Handling ---
class WikipediaToolInput(BaseModel):
    query: str = Field(description="The search query for Wikipedia.")

class RobustWikipediaTool(BaseTool):
    name: str = "wikipedia"
    description: str = "A wrapper around Wikipedia. Useful for when you need to answer general questions about people, places, companies, facts, historical events, or other subjects. Input should be a search query."
    args_schema: Type[BaseModel] = WikipediaToolInput
    
    def _run(self, query: str) -> str:
        """Use the Wikipedia tool."""
        try:
            wiki = WikipediaAPIWrapper()
            return wiki.run(query)
        except Exception as e:
            return f"Error fetching from Wikipedia: {str(e)}. Please try a different query or tool."

    async def _arun(self, query: str) -> str:
        """Use the Wikipedia tool asynchronously."""
        try:
            wiki = WikipediaAPIWrapper()
            return wiki.run(query)
        except Exception as e:
            return f"Error fetching from Wikipedia: {str(e)}. Please try a different query or tool."

# --- Tavily Tool ---
def get_tavily_tool():
    return TavilySearchResults()

# --- Stock Price Tool (via yfinance) ---
import yfinance as yf
import matplotlib.pyplot as plt
import io
import chainlit as cl

# Use non-interactive backend for server environments
plt.switch_backend('Agg')

class StockPriceInput(BaseModel):
    symbol: str = Field(description="The stock symbol to look up (e.g., 'AAPL', 'MSFT').")

class StockPriceTool(BaseTool):
    name: str = "get_stock_price"
    description: str = "Useful for getting the latest stock price data for a given symbol. Returns the latest price and currency."
    args_schema: Type[BaseModel] = StockPriceInput

    def _run(self, symbol: str) -> str:
        try:
            ticker = yf.Ticker(symbol)
            
            # 1. Get Current Price (Fast)
            price = ticker.fast_info.last_price
            currency = ticker.fast_info.currency
            
            # 2. Get Historical Data for Chart (3 Months for better trend)
            hist = ticker.history(period="3mo")
            
            if not hist.empty:
                # Calculate simple metrics
                hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
                volatility = hist['Close'].std()
                
                # Create the plot
                plt.figure(figsize=(10, 6))
                plt.plot(hist.index, hist['Close'], label='Close Price', linewidth=2)
                plt.plot(hist.index, hist['SMA_20'], label='20-Day SMA', linestyle='--', alpha=0.7)
                
                plt.title(f'{symbol} Price Trend & Moving Average (Last 3 Months)')
                plt.xlabel('Date')
                plt.ylabel(f'Price ({currency})')
                plt.grid(True, alpha=0.3)
                plt.legend()
                
                # Add text annotation for volatility
                plt.figtext(0.15, 0.85, f'Volatility (Std Dev): {volatility:.2f}', fontsize=10, bbox=dict(facecolor='white', alpha=0.8))
                
                # Save plot to bytes
                buf = io.BytesIO()
                plt.savefig(buf, format='png', dpi=100)
                buf.seek(0)
                plt.close() # Clean up memory
                
                # Send to Chainlit UI (Async call from Sync context)
                image = cl.Image(content=buf.getvalue(), name=f"{symbol}_stock_chart", display="inline")
                cl.run_sync(cl.Message(content=f"Here is the market analysis chart for {symbol} (including 20-day Moving Average):", elements=[image]).send())

            # Fallback for price if fast_info failed
            if price is None and not hist.empty:
                price = hist['Close'].iloc[-1]
                currency = "USD"

            if price:
                return f"The current price of {symbol} is {price:.2f} {currency}."
            else:
                return f"Could not fetch price for {symbol}. The symbol might be invalid."
                
        except Exception as e:
            return f"Error fetching stock data for {symbol}: {str(e)}"

    async def _arun(self, symbol: str) -> str:
        # yfinance is synchronous
        return self._run(symbol)

def get_tools():
    return [
        RobustWikipediaTool(),
        get_tavily_tool(),
        StockPriceTool()
    ]
