import os
from utils.weather_info import WeatherForecastTool
from langchain.tools import tool
from typing import List
from dotenv import load_dotenv

class WeatherInfoTool:
    def __init__(self):
        load_dotenv()
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")
        self.weather_service= WeatherForecastTool(api=self.api_key) 
        self.weather_tool_list=self._setup_tools()
    
    def _setup_tools(self) -> List:
        @tool
        def get_current_weather(place: str) -> dict:
            """Get current weather information for a specified place."""
            weather_data= self.weather_service.get_weather(place)
            if weather_data:
                temp= weather_data.get('main', {}).get('temp',"N/A")
                description= weather_data.get('weather', [{}])[0].get('description',"N/A")
                humidity= weather_data.get('main', {}).get('humidity',"N/A")
                return f"Current weather in {place}: Temperature: {temp}°C, Description: {description}, Humidity: {humidity}%"
            return {"error": f"Could not retrieve weather data for {place}."}
        @tool
        def get_weather_forecast(place: str) -> str:
            """Get weather forecast for a specified place."""
            forecast_data= self.weather_service.get_forecast_weather(place)
            if forecast_data and 'list' in forecast_data:
                forecast_summary = []
                for i in range(len(forecast_data['list'])):
                    item = forecast_data['list'][i]
                    date = item['dt_txt'].split(' ')[0]
                    temp = item['main']['temp']
                    desc = item['weather'][0]['description']
                    forecast_summary.append(f"{date}: {temp} degree celcius , {desc}")
                return f"Weather forecast for {place}:\n" + "\n".join(forecast_summary)
            return f"Could not fetch forecast for {place}"
    
        return [get_current_weather, get_weather_forecast]