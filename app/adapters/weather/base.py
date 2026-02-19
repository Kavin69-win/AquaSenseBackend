from abc import ABC, abstractmethod
from app.schemas.weather import WeatherData

class WeatherProviderStrategy(ABC):
    """
    Abstract Base Class for Weather Data Providers.
    Any new weather service (OpenMeteo, IMD, etc.) must inherit from this
    and implement the 'get_district_weather' method.
    """

    @abstractmethod
    async def get_district_weather(self, district_name: str) -> WeatherData:
        """
        Fetches current weather and forecast for a specific district.
        
        Args:
            district_name (str): The target district (e.g., "Ludhiana")
            
        Returns:
            WeatherData: A normalized Pydantic object containing SI unit metrics.
            
        Raises:
            WeatherServiceException: If the external API is unreachable or returns invalid data.
        """
        pass