import pytest
from schemas import DailyWeather, HourlyWeather
from services.agronomic import AgronomicLogic

@pytest.fixture
def agronomic_logic():
    return AgronomicLogic()

def test_generate_diagnostics_sprouting_cold(agronomic_logic):
    
    current_weather = {"temperature": 15, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[0], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Clear"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[36], relativehumidity_2m=[50], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Clear"]
    )
    
    diagnostics = agronomic_logic.generate_diagnostics(current_weather, daily, hourly)
  
    sprouting_diag = diagnostics[0]["sprouting"]
    
    assert any(d["title"] == "Emergência Lenta" for d in sprouting_diag)
    assert any("Solo frio" in d["message"] for d in sprouting_diag)

def test_generate_tips_sprouting_cold(agronomic_logic):

    current_weather = {"temperature": 15, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[0], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Clear"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[15], relativehumidity_2m=[50], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Clear"]
    )
    
    tips = agronomic_logic.generate_tips(current_weather, daily, hourly)
    sprouting_tips = tips[0]["sprouting"]
    
  
    assert any("Emergência Lenta" in t["message"] for t in sprouting_tips)

def test_generate_diagnostics_growth_heat(agronomic_logic):

    current_weather = {"temperature": 36, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[0], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Clear"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[36], relativehumidity_2m=[50], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Clear"]
    )
    
    diagnostics = agronomic_logic.generate_diagnostics(current_weather, daily, hourly)
    growth_diag = diagnostics[0]["growth"]
    
    assert any(d["title"] == "Estresse Térmico" for d in growth_diag)

def test_generate_tips_growth_heat(agronomic_logic):
  
    current_weather = {"temperature": 36, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[0], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Clear"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[36], relativehumidity_2m=[50], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Clear"]
    )
    
    tips = agronomic_logic.generate_tips(current_weather, daily, hourly)
    growth_tips = tips[0]["growth"]
    
    assert any("Alerta de Respiração" in t["message"] for t in growth_tips)

def test_generate_diagnostics_ripening_rain(agronomic_logic):
 
    current_weather = {"temperature": 25, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[25], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Rain"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[25], relativehumidity_2m=[80], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Rain"]
    )
    
    diagnostics = agronomic_logic.generate_diagnostics(current_weather, daily, hourly)
    ripening_diag = diagnostics[0]["ripening"]
    
    assert any(d["title"] == "Queda de ATR" for d in ripening_diag)

def test_generate_tips_ripening_rain(agronomic_logic):
 
    current_weather = {"temperature": 25, "windspeed": 5}
    daily = DailyWeather(
        time=["2023-10-01"], precipitation_sum=[35], et0_fao_evapotranspiration=[0], 
        shortwave_radiation_sum=[20], weathercode=[0], weather_description=["Rain"]
    )
    hourly = HourlyWeather(
        time=["2023-10-01T00:00"], temperature_2m=[25], relativehumidity_2m=[80], 
        windspeed_10m=[5], weathercode=[0], soil_moisture_0_to_1cm=[0.3], 
        soil_moisture_27_to_81cm=[0.3], weather_description=["Rain"]
    )
    
    tips = agronomic_logic.generate_tips(current_weather, daily, hourly)
    ripening_tips = tips[0]["ripening"]
    
    assert any("Suspender Colheita" in t["message"] for t in ripening_tips)
