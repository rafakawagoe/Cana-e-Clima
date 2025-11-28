from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Coordinates(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None

class DailyWeather(BaseModel):
    time: List[str]
    precipitation_sum: List[Optional[float]]
    et0_fao_evapotranspiration: List[Optional[float]]
    shortwave_radiation_sum: List[Optional[float]]

class HourlyWeather(BaseModel):
    time: List[str]
    soil_moisture_0_to_1cm: List[Optional[float]]
    soil_moisture_27_to_81cm: List[Optional[float]]

class WeatherResponse(BaseModel):
    city: str
    country: Optional[str]
    latitude: float
    longitude: float
    weather: Dict[str, Any]
    daily: Optional[DailyWeather] = None
    hourly: Optional[HourlyWeather] = None
