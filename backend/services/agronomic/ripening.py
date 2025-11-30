from typing import List, Dict, Any
from schemas import DailyWeather, HourlyWeather

class RipeningAnalyzer:
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

        today_rain = get_daily_val("precipitation_sum") or 0
        if today_rain > 20:
            diagnostics.append({
                "title": "Queda de ATR",
                "message": "Chuva na maturação inverte sacarose e dificulta colheita.",
                "type": "danger"
            })

        day_temps = get_hourly_slice("temperature_2m")
        day_moisture = get_hourly_slice("soil_moisture_0_to_1cm")
        recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)

        if day_temps and recent_moisture is not None:
            if min(day_temps) > 18 and recent_moisture > 0.40:
                diagnostics.append({
                    "title": "Risco de Florescimento",
                    "message": "Noites quentes e umidade induzem isoporização.",
                    "type": "warning"
                })

        if day_temps and min(day_temps) < 2:
            diagnostics.append({
                "title": "Alerta de Geada",
                "message": "Risco iminente de morte da gema apical.",
                "type": "danger"
            })

        if day_temps:
            amplitude = max(day_temps) - min(day_temps)
            if amplitude > 10:
                diagnostics.append({
                    "title": "Pico de Sacarose",
                    "message": "Condições perfeitas para acúmulo de ATR.",
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

        today_rain = get_daily_val("precipitation_sum") or 0
        if today_rain > 30:
            tips.append({
                "message": "🛑 Suspender Colheita: Chuva inverte sacarose e compacta solo.",
                "type": "danger"
            })

        day_temps = get_hourly_slice("temperature_2m")
        if day_temps:
            amplitude = max(day_temps) - min(day_temps)
            if amplitude > 10:
                tips.append({
                    "message": "💰 Pico de Açúcar: Amplitude térmica favorece acúmulo de ATR.",
                    "type": "success"
                })

        day_moisture = get_hourly_slice("soil_moisture_0_to_1cm")
        recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)

        if day_temps and min(day_temps) > 18 and recent_moisture is not None and recent_moisture > 0.40:
                tips.append({
                "message": "🌸 RISCO DE FLORESCIMENTO: Calor e umidade induzem florada.",
                "type": "warning"
            })

        if day_temps and min(day_temps) < 5:
            tips.append({
                "message": "❄️ Alerta de Geada: Risco de morte da gema apical.",
                "type": "danger"
            })
        
        return tips
