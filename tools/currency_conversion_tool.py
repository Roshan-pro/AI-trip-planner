import os
from dotenv import load_dotenv
from openai import api_key
from utils.currency_converter import CurrencyConverter
from typing import List
from langchain.tools import tool

class CurrencyConversionTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("EXCHANGE_RATE_API_KEY")
        self.converter = CurrencyConverter(self.api_key)
        self.currency_tool_list = self._setup_tools()
    def _setup_tools(self) -> List:
        @tool(name_or_callable="convert_currency", description="Converts an amount from one currency to another.")
        def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
            """Convert amount from one currency to another."""
            return self.converter.convert(from_currency, to_currency, amount)
        
        @tool(name_or_callable="get_supported_currencies", description="Gets a list of supported currencies for conversion.")
        def get_supported_currencies23() -> float:
            """Get the exchange rate between two currencies."""
            return self.converter.get_supported_currencies()
        
        return [convert_currency, get_supported_currencies23]