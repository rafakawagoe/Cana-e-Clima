from fastapi.testclient import TestClient
from main import app
from unittest.mock import patch, AsyncMock
from schemas import Coordinates

client = TestClient(app)

# Mock data
MOCK_COORDINATES = Coordinates(
    name="Ribeirão Preto",
    latitude=-21.1775,
    longitude=-47.8103,
    country="Brazil",
    state="São Paulo"
)

MOCK_WEATHER_DATA = {
    "current_weather": {"temperature": 25, "weathercode": 0, "windspeed": 10},
    "hourly": {
        "time": ["2023-10-01T00:00"],
        "temperature_2m": [25],
        "relativehumidity_2m": [60],
        "windspeed_10m": [10],
        "weathercode": [0],
        "soil_moisture_0_to_1cm": [0.3],
        "soil_moisture_27_to_81cm": [0.3]
    },
    "daily": {
        "time": ["2023-10-01"],
        "precipitation_sum": [0],
        "et0_fao_evapotranspiration": [5],
        "shortwave_radiation_sum": [20],
        "weathercode": [0]
    }
}

@patch("services.open_meteo.OpenMeteoService.get_coordinates", new_callable=AsyncMock)
@patch("services.open_meteo.OpenMeteoService.get_weather", new_callable=AsyncMock)
def test_get_weather_success(mock_get_weather, mock_get_coordinates):
    mock_get_coordinates.return_value = MOCK_COORDINATES
    mock_get_weather.return_value = MOCK_WEATHER_DATA

    response = client.get("/weather/Ribeirão Preto")
    
    assert response.status_code == 200
    data = response.json()
    assert data["city"] == "Ribeirão Preto"
    assert "diagnostics" in data
    assert "agronomic_tips" in data
