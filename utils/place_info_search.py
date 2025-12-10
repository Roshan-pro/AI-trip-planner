import os 
import json
from langchain_tavily import TavilySearch


class TavilyPlaceSearchTool:
    def __init__(self):
        pass
    def tavily_search_attractions(self,place:str)->dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"Top attractions places in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_restaurants(self,place:str)->dict:
        """
        Searches for restaurants in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_hotels(self,place:str)->dict:
        """
        Searches for hotels in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the top 10 hotels and accommodations in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_transportation(self,place:str)->dict:
        """
        Searches for transportation options in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the best transportation options in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_nightlife(self,place:str)->dict:
        """
        Searches for nightlife options in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the top nightlife and entertainment options in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_shopping(self,place:str)->dict:
        """
        Searches for shopping options in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the best shopping areas and markets in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    def tavily_search_hospitals(self,place:str)->dict:
        """
        Searches for hospitals in the specified place using TavilySearch.
        """
        tavily_tool =TavilySearch(topic="general",include_answers="advanced")
        try:
            results = tavily_tool.invoke({"query": f"what are the top hospitals and medical facilities in and around {place}"} )
            return results["answer"]
        except Exception as e:
            return {"error": str(e)}
    