import os 
from utils.place_info_search import TavilyPlaceSearchTool
from typing import List
from langchain.tools import tool

class PlaceSearchTool:
    def __init__(self):
        self.tavily_search = TavilyPlaceSearchTool()
        self.place_search_tool = self._setup_tool()

    def _setup_tool(self)-> list:
        """Sets up the list of place search tools."""
        @tool(name_or_callable="search_attractions", description="Searches for attractions in the specified place.")
        def search_attractions(place: str) -> dict:
            """Searches for attractions in the specified place."""
            return self.tavily_search.tavily_search_attractions(place)
        @tool(name_or_callable="search_restaurants", description="Searches for restaurants in the specified place.")
        def search_restaurants(place: str) -> dict:
            """Searches for restaurants in the specified place."""
            return self.tavily_search.tavily_search_restaurants(place)
        @tool(name_or_callable="search_hotels", description="Searches for hotels in the specified place.")
        def search_hotels(place: str) -> dict:
            """Searches for hotels in the specified place."""
            return self.tavily_search.tavily_search_hotels(place)      
        @tool(name_or_callable="search_transportation", description="Searches for transportation options in the specified place.")
        def search_transportation(place: str) -> dict:
            """Searches for transportation options in the specified place."""
            return self.tavily_search.tavily_search_transportation(place)
        
        @tool(name_or_callable="search_nightlife", description="Searches for nightlife options in the specified place.")
        def search_nightlife(place: str) -> dict:
            """Searches for nightlife options in the specified place."""
            return self.tavily_search.tavily_search_nightlife(place)    
        @tool(name_or_callable="search_shopping", description="Searches for shopping options in the specified place.")
        def search_shopping(place: str) -> dict:    
            """Searches for shopping options in the specified place."""
            return self.tavily_search.tavily_search_shopping(place)    
        @tool(name_or_callable="search_hospitals", description="Searches for hospitals in the specified place.")
        def search_hospitals(place: str) -> dict:
            """Searches for hospitals in the specified place."""
            return self.tavily_search.tavily_search_hospitals(place)
        
        return [
            search_attractions,
            search_restaurants,
            search_hotels,
            search_transportation,
            search_nightlife,
            search_shopping,
            search_hospitals
        ]