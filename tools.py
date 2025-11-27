import os
from typing import Optional, Type
from langchain_core.tools import Tool, BaseTool
from langchain_community.tools import TavilySearchResults
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field
from alpha_vantage.timeseries import TimeSeries

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

# --- Alpha Vantage Tool ---
class AlphaVantageInput(BaseModel):
    symbol: str = Field(description="The stock symbol to look up (e.g., 'AAPL', 'MSFT').")

class AlphaVantageTool(BaseTool):
    name: str = "alpha_vantage_stock_price"
    description: str = "Useful for getting the latest stock price data for a given symbol using Alpha Vantage. Returns the latest daily close price."
    args_schema: Type[BaseModel] = AlphaVantageInput

    def _run(self, symbol: str) -> str:
        api_key = os.getenv("ALPHAVANTAGE_API_KEY")
        if not api_key:
            return "Error: ALPHAVANTAGE_API_KEY not found in environment variables."
        
        try:
            ts = TimeSeries(key=api_key, output_format='pandas')
            data, meta_data = ts.get_daily(symbol=symbol, outputsize='compact')
            # Get the latest row
            latest_date = data.index[0]
            latest_close = data.iloc[0]['4. close']
            return f"The latest closing price for {symbol} on {latest_date} was ${latest_close}."
        except Exception as e:
            return f"Error fetching stock data for {symbol}: {str(e)}"

    async def _arun(self, symbol: str) -> str:
        # Alpha Vantage library is synchronous, so we wrap the sync call
        return self._run(symbol)

def get_tools():
    return [
        RobustWikipediaTool(),
        get_tavily_tool(),
        AlphaVantageTool()
    ]
