from typing import Dict

WEATHER_DESCRIPTIONS: Dict[int, str] = {
    0: 'Céu Limpo',
    1: 'Principalmente Limpo',
    2: 'Parcialmente Nublado',
    3: 'Encoberto',
    45: 'Nevoeiro',
    48: 'Nevoeiro com Geada',
    51: 'Chuvisco Leve',
    53: 'Chuvisco Moderado',
    55: 'Chuvisco Denso',
    56: 'Chuvisco Congelante Leve',
    57: 'Chuvisco Congelante Denso',
    61: 'Chuva Fraca',
    63: 'Chuva Moderada',
    65: 'Chuva Forte',
    66: 'Chuva Congelante Leve',
    67: 'Chuva Congelante Forte',
    71: 'Neve Fraca',
    73: 'Neve Moderada',
    75: 'Neve Forte',
    77: 'Grãos de Neve',
    80: 'Pancadas de Chuva Fraca',
    81: 'Pancadas de Chuva Moderada',
    82: 'Pancadas de Chuva Violenta',
    85: 'Pancadas de Neve Fraca',
    86: 'Pancadas de Neve Forte',
    95: 'Tempestade',
    96: 'Tempestade com Granizo Leve',
    99: 'Tempestade com Granizo Forte'
}

def get_weather_description(code: int) -> str:
    return WEATHER_DESCRIPTIONS.get(code, 'Desconhecido')

OPEN_METEO_HOURLY_PARAMS = "temperature_2m,relativehumidity_2m,windspeed_10m,weathercode,soil_moisture_0_to_1cm,soil_moisture_27_to_81cm"
OPEN_METEO_DAILY_PARAMS = "precipitation_sum,et0_fao_evapotranspiration,shortwave_radiation_sum,weathercode"
