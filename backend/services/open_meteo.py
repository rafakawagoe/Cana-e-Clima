import httpx
import logging
from fastapi import HTTPException
from cachetools import TTLCache, cached
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception
from config import settings
from schemas import Coordinates
from constants import get_weather_description, OPEN_METEO_HOURLY_PARAMS, OPEN_METEO_DAILY_PARAMS

logger = logging.getLogger(__name__)

def is_retryable(e):
    return not (isinstance(e, HTTPException) and e.status_code == 404)

class OpenMeteoService:
  
    cache = TTLCache(maxsize=100, ttl=3600)

    @cached(cache)
    @retry(
        stop=stop_after_attempt(3), 
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception(is_retryable)
    )
    async def get_coordinates(self, city_name: str) -> Coordinates:
      
        logger.info(f"Fetching coordinates for city: {city_name}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.OPEN_METEO_GEOCODING_URL,
                    params={"name": city_name, "count": 1, "language": "pt", "format": "json"}
                )
                response.raise_for_status()
                data = response.json()
                
                if not data.get("results"):
                    logger.warning(f"City not found: {city_name}")
                    raise HTTPException(status_code=404, detail="City not found")
                
                result = data["results"][0]
                logger.info(f"Found coordinates for {city_name}: {result['latitude']}, {result['longitude']}")
                return Coordinates(
                    name=result["name"],
                    latitude=result["latitude"],
                    longitude=result["longitude"],
                    country=result.get("country"),
                    state=result.get("admin1")
                )
            except httpx.RequestError as e:
                logger.error(f"Error connecting to geocoding service: {str(e)}")
                raise HTTPException(status_code=503, detail=f"Error connecting to geocoding service: {str(e)}")

    @cached(cache)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_weather(self, lat: float, lon: float) -> dict:
     
        logger.info(f"Fetching weather data for coordinates: {lat}, {lon}")
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.OPEN_METEO_WEATHER_URL,
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current_weather": True,
                        "hourly": OPEN_METEO_HOURLY_PARAMS,
                        "daily": OPEN_METEO_DAILY_PARAMS,
                        "timezone": "auto"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                logger.error(f"Error connecting to weather service: {str(e)}")
                raise HTTPException(status_code=503, detail=f"Error connecting to weather service: {str(e)}")

    def enrich_weather_data(self, weather_data: dict) -> dict:
        
        if weather_data.get("hourly"):
            weather_data["hourly"]["weather_description"] = [
                get_weather_description(code) 
                for code in weather_data["hourly"].get("weathercode", [])
            ]

        if weather_data.get("daily"):
            weather_data["daily"]["weather_description"] = [
                get_weather_description(code) 
                for code in weather_data["daily"].get("weathercode", [])
            ]
            
        return weather_data
