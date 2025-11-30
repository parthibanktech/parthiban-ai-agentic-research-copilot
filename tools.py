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

class StockPriceInput(BaseModel):
    symbol: str = Field(description="The stock symbol to look up (e.g., 'AAPL', 'MSFT').")

class StockPriceTool(BaseTool):
    name: str = "get_stock_price"
    description: str = "Useful for getting the latest stock price data for a given symbol. Returns the latest price and currency."
    args_schema: Type[BaseModel] = StockPriceInput

    def _run(self, symbol: str) -> str:
        try:
            ticker = yf.Ticker(symbol)
            # fast_info is often faster and more reliable for current price than history()
            price = ticker.fast_info.last_price
            currency = ticker.fast_info.currency
            
            if price is None:
                # Fallback to history if fast_info fails
                hist = ticker.history(period="1d")
                if not hist.empty:
                    price = hist['Close'].iloc[-1]
                    currency = "USD" # Assumption if not found
            
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
