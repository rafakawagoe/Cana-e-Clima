from typing import List, Dict, Any
from schemas import DailyWeather, HourlyWeather

class GrowthAnalyzer:
    def analyze_diagnostics(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather, day_index: int, is_today: bool) -> List[Dict[str, str]]:
        diagnostics = []

        def get_daily_val(attr):
            val_list = getattr(daily, attr, None)
            return val_list[day_index] if val_list and len(val_list) > day_index else None

        def get_hourly_slice(attr):
            val_list = getattr(hourly, attr, None)
            if not val_list: return []
            start = day_index * 24
            end = start + 24
            return [x for x in val_list[start:end] if x is not None]

        day_root_moisture = get_hourly_slice("soil_moisture_27_to_81cm")
        recent_root_moisture = day_root_moisture[12] if len(day_root_moisture) > 12 else (day_root_moisture[0] if day_root_moisture else None)

        if recent_root_moisture is not None and recent_root_moisture < 0.30:
            diagnostics.append({
                "title": "Quebra de TCH",
                "message": "Déficit hídrico severo. Alongamento de colmos comprometido.",
                "type": "danger"
            })

        day_temps = get_hourly_slice("temperature_2m")
        if day_temps and max(day_temps) > 35:
            diagnostics.append({
                "title": "Estresse Térmico",
                "message": "Respiração excessiva consome sacarose. Planta gasta energia para resfriar.",
                "type": "warning"
            })

        today_rad = get_daily_val("shortwave_radiation_sum")
        if today_rad is not None and today_rad < 15:
            diagnostics.append({
                "title": "Baixa Fotossíntese",
                "message": "Pouca luz reduz a eficiência C4. Crescimento limitado.",
                "type": "warning"
            })

        if is_today:
            current_wind = current_weather.get("windspeed")
            if current_wind is not None and current_wind > 10:
                diagnostics.append({
                    "title": "Parar Pulverização",
                    "message": "Risco alto de deriva. Suspenda aplicações.",
                    "type": "danger"
                })
        else:
                day_winds = get_hourly_slice("windspeed_10m")
                if day_winds and max(day_winds) > 15:
                    diagnostics.append({
                    "title": "Vento Forte Previsto",
                    "message": "Rajadas de vento podem impedir pulverização.",
                    "type": "warning"
                })

        if recent_root_moisture is not None and recent_root_moisture >= 0.30 and today_rad is not None and today_rad > 20:
                diagnostics.append({
                "title": "Máximo Crescimento",
                "message": "Taxa fotossintética plena. Aproveite para adubação.",
                "type": "success"
            })
        
        return diagnostics

    def analyze_tips(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather, day_index: int, is_today: bool) -> List[Dict[str, str]]:
        tips = []

        def get_daily_val(attr):
            val_list = getattr(daily, attr, None)
            return val_list[day_index] if val_list and len(val_list) > day_index else None

        def get_hourly_slice(attr):
            val_list = getattr(hourly, attr, None)
            if not val_list: return []
            start = day_index * 24
            end = start + 24
            return [x for x in val_list[start:end] if x is not None]

        day_temps = get_hourly_slice("temperature_2m")
        if day_temps and max(day_temps) > 35:
            tips.append({
                "message": "🔥 Alerta de Respiração: Altas temperaturas consomem sacarose.",
                "type": "warning"
            })

        today_rad = get_daily_val("shortwave_radiation_sum")
        if today_rad is not None and today_rad < 15:
            tips.append({
                "message": "☁️ Baixa Fotossíntese: Dias nublados reduzem o crescimento.",
                "type": "info"
            })

        day_root_moisture = get_hourly_slice("soil_moisture_27_to_81cm")
        recent_root_moisture = day_root_moisture[12] if len(day_root_moisture) > 12 else (day_root_moisture[0] if day_root_moisture else None)

        if recent_root_moisture is not None and recent_root_moisture < 0.30:
            tips.append({
                "message": "📉 Perda de TCH: Déficit hídrico gera colmos curtos.",
                "type": "danger"
            })

        if is_today:
            current_wind = current_weather.get("windspeed")
            if current_wind is not None and current_wind > 10:
                tips.append({
                    "message": "🚫 Parar Pulverização: Vento forte. Risco de deriva.",
                    "type": "danger"
                })
        
        return tips
