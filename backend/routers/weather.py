from fastapi import APIRouter, Depends, Path
from services.open_meteo import OpenMeteoService
from services.agronomic import AgronomicLogic
from schemas import WeatherResponse, DailyWeather, HourlyWeather
from constants import get_weather_description

router = APIRouter(
    prefix="/weather",
    tags=["weather"],
    responses={404: {"description": "Not found"}},
)

def get_open_meteo_service():
    return OpenMeteoService()

def get_agronomic_logic():
    return AgronomicLogic()

@router.get("/{city_name}", response_model=WeatherResponse)
async def get_weather(
    city_name: str = Path(..., min_length=2, description="Nome da cidade para busca"), 
    service: OpenMeteoService = Depends(get_open_meteo_service),
    agronomic_service: AgronomicLogic = Depends(get_agronomic_logic)
):
    coordinates = await service.get_coordinates(city_name)
    weather_data = await service.get_weather(coordinates.latitude, coordinates.longitude)
    
    weather_data = service.enrich_weather_data(weather_data)
    
    current_weather_code = weather_data.get("current_weather", {}).get("weathercode", 0)

    daily_data = DailyWeather(**weather_data.get("daily")) if weather_data.get("daily") else None
    hourly_data = HourlyWeather(**weather_data.get("hourly")) if weather_data.get("hourly") else None
    
    tips = agronomic_service.generate_tips(
        weather_data.get("current_weather", {}),
        daily_data,
        hourly_data
    )

    diagnostics = agronomic_service.generate_diagnostics(
        weather_data.get("current_weather", {}),
        daily_data,
        hourly_data
    )

    return WeatherResponse(
        city=coordinates.name,
        country=coordinates.country,
        state=coordinates.state,
        latitude=coordinates.latitude,
        longitude=coordinates.longitude,
        weather=weather_data.get("current_weather", {}),
        condition_description=get_weather_description(current_weather_code),
        daily=weather_data.get("daily"),
        hourly=weather_data.get("hourly"),
        agronomic_tips=tips,
        diagnostics=diagnostics
    )
