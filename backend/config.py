from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPEN_METEO_GEOCODING_URL: str = "https://geocoding-api.open-meteo.com/v1/search"
    OPEN_METEO_WEATHER_URL: str = "https://api.open-meteo.com/v1/forecast"

    class Config:
        env_file = ".env"

settings = Settings()
