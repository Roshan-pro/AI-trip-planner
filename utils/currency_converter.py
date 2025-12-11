import requests
class CurrencyConverter:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://v6.exchangerate-api.com/v6/"

    def convert(self, from_currency: str, to_currency: str, amount: float) -> dict:
        """Convert amount from one currency to another."""
        try:
            url = f"{self.base_url}{self.api_key}/latest/{from_currency}/{to_currency}/{amount}"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching conversion data: {response.status_code}, {response.text}")
        except Exception as e:
            return {"error": str(e)}

    def get_supported_currencies(self) -> dict:
        """Get a list of supported currencies."""
        try:
            url = f"{self.base_url}{self.api_key}/codes"
            response = requests.get(url)
            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Error fetching supported currencies: {response.status_code}, {response.text}")
        except Exception as e:
            return {"error": str(e)}