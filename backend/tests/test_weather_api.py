import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock, patch
import pytest
from schemas import Coordinates

try:
    client = TestClient(app)
except Exception as e:
    print(f"Error instantiating TestClient: {e}")
    raise e


def test_get_weather_success():
    mock_coordinates = Coordinates(
        name="London",
        country="United Kingdom",
        latitude=51.5074,
        longitude=-0.1278
    )
    mock_weather_data = {
        "current_weather": {
            "temperature": 15.0,
            "windspeed": 10.0,
            "winddirection": 200,
            "weathercode": 1,
            "time": "2023-10-27T12:00"
        },
        "daily": {
            "time": ["2023-10-27"],
            "precipitation_sum": [5.0],
            "et0_fao_evapotranspiration": [3.5],
            "shortwave_radiation_sum": [15.0],
            "weathercode": [1],
            "weather_description": ["Mainly Clear"]
        },
        "hourly": {
            "time": ["2023-10-27T00:00"],
            "soil_moisture_0_to_1cm": [0.3],
            "soil_moisture_27_to_81cm": [0.4],
            "temperature_2m": [20.0],
            "relativehumidity_2m": [60.0],
            "windspeed_10m": [10.0],
            "weathercode": [1],
            "weather_description": ["Mainly Clear"]
        }
    }

    with patch("routers.weather.OpenMeteoService.get_coordinates", new_callable=AsyncMock) as mock_get_coords, \
         patch("routers.weather.OpenMeteoService.get_weather", new_callable=AsyncMock) as mock_get_weather:
        
        mock_get_coords.return_value = mock_coordinates
        mock_get_weather.return_value = mock_weather_data

        response = client.get("/weather/London")
        
        assert response.status_code == 200
        data = response.json()
        assert data["city"] == "London"
        assert data["latitude"] == 51.5074
        assert data["weather"] == mock_weather_data["current_weather"]
        assert data["daily"]["precipitation_sum"] == [5.0]
        assert data["hourly"]["soil_moisture_0_to_1cm"] == [0.3]
        assert data["hourly"]["temperature_2m"] == [20.0]

def test_get_weather_city_not_found():
    with patch("routers.weather.OpenMeteoService.get_coordinates", new_callable=AsyncMock) as mock_get_coords:
        from fastapi import HTTPException
        mock_get_coords.side_effect = HTTPException(status_code=404, detail="City not found")

        response = client.get("/weather/NonExistentCity")
        
        assert response.status_code == 404
        assert response.json()["detail"] == "City not found"

