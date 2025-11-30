from pydantic import BaseModel
from typing import Optional, Dict, Any, List

class Coordinates(BaseModel):
    name: str
    latitude: float
    longitude: float
    country: Optional[str] = None
    state: Optional[str] = None

class DailyWeather(BaseModel):
    time: List[str]
    precipitation_sum: List[Optional[float]]
    et0_fao_evapotranspiration: List[Optional[float]]
    shortwave_radiation_sum: List[Optional[float]]
    weathercode: List[Optional[int]]
    weather_description: List[str]

class HourlyWeather(BaseModel):
    time: List[str]
    temperature_2m: List[Optional[float]]
    relativehumidity_2m: List[Optional[float]]
    windspeed_10m: List[Optional[float]]
    weathercode: List[Optional[int]]
    soil_moisture_0_to_1cm: List[Optional[float]]
    soil_moisture_27_to_81cm: List[Optional[float]]
    weather_description: List[str]

class AgronomicTip(BaseModel):
    message: str
    type: str 

class Diagnostic(BaseModel):
    title: str
    message: str
    type: str 

class WeatherResponse(BaseModel):
    city: str
    country: Optional[str]
    state: Optional[str]
    latitude: float
    longitude: float
    weather: Dict[str, Any]
    condition_description: str
    daily: Optional[DailyWeather] = None
    hourly: Optional[HourlyWeather] = None
    agronomic_tips: Optional[List[Dict[str, List[AgronomicTip]]]] = None
    diagnostics: Optional[List[Dict[str, List[Diagnostic]]]] = None
