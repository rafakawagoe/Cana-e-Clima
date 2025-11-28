import httpx
from fastapi import HTTPException
from cachetools import TTLCache, cached
from tenacity import retry, stop_after_attempt, wait_exponential
from config import settings
from schemas import Coordinates

class OpenMeteoService:
    cache = TTLCache(maxsize=100, ttl=3600)

    @cached(cache)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_coordinates(self, city_name: str) -> Coordinates:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.OPEN_METEO_GEOCODING_URL,
                    params={"name": city_name, "count": 1, "language": "pt", "format": "json"}
                )
                response.raise_for_status()
                data = response.json()
                
                if not data.get("results"):
                    raise HTTPException(status_code=404, detail="City not found")
                
                result = data["results"][0]
                return Coordinates(
                    name=result["name"],
                    latitude=result["latitude"],
                    longitude=result["longitude"],
                    country=result.get("country")
                )
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Error connecting to geocoding service: {str(e)}")

    @cached(cache)
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    async def get_weather(self, lat: float, lon: float):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.OPEN_METEO_WEATHER_URL,
                    params={
                        "latitude": lat,
                        "longitude": lon,
                        "current_weather": True,
                        "hourly": "temperature_2m,relativehumidity_2m,windspeed_10m,soil_moisture_0_to_1cm,soil_moisture_27_to_81cm",
                        "daily": "precipitation_sum,et0_fao_evapotranspiration,shortwave_radiation_sum",
                        "timezone": "auto"
                    }
                )
                response.raise_for_status()
                return response.json()
            except httpx.RequestError as e:
                raise HTTPException(status_code=503, detail=f"Error connecting to weather service: {str(e)}")
