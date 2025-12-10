import requests

class WeatherForecastTool:
    def __init__(self, api : str):
        self.api_key= api
        self.base_url = "http://api.openweathermap.org/data/2.5/weather"
        
    def get_weather(self, place: str) -> dict:
        """Fetch weather information for a given place."""
        try:        
                params = {
                    'q': place,
                    'appid': self.api_key
                }
                response = requests.get(self.base_url, params=params)
                if response.status_code == 200:
                    return response.json()
                else:
                    raise Exception(f"Error fetching weather data: {response.status_code}, {response.text}")            
        except Exception as e:
            return {"error": str(e)}
    def get_forecast_weather(self, place: str) -> str:
        """Get a formatted weather forecast for a given place."""
        try:
            params={
                'q': place,
                'appid': self.api_key,
                'units': 'metric',
                'cnt': 10
            }
            response = requests.get(self.base_url, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching weather data: {response.status_code}, {response.text}")
            
        except Exception as e:  
            return {"error": str(e)}