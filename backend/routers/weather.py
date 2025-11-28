from fastapi import APIRouter, Depends
from services.open_meteo import OpenMeteoService
from schemas import WeatherResponse

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

def get_open_meteo_service():
    return OpenMeteoService()

@router.get("/{city_name}", response_model=WeatherResponse)
async def get_weather(city_name: str, service: OpenMeteoService = Depends(get_open_meteo_service)):
    coordinates = await service.get_coordinates(city_name)
    weather_data = await service.get_weather(coordinates.latitude, coordinates.longitude)
    
    return WeatherResponse(
        city=coordinates.name,
        country=coordinates.country,
        latitude=coordinates.latitude,
        longitude=coordinates.longitude,
        weather=weather_data.get("current_weather", {}),
        daily=weather_data.get("daily"),
        hourly=weather_data.get("hourly")
    )
