from typing import List, Dict, Any
from schemas import DailyWeather, HourlyWeather

class SproutingAnalyzer:
    def analyze_diagnostics(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather, day_index: int, is_today: bool) -> List[Dict[str, str]]:
        diagnostics = []

        # Helper to get hourly values
        def get_hourly_slice(attr):
            val_list = getattr(hourly, attr, None)
            if not val_list: return []
            start = day_index * 24
            end = start + 24
            return [x for x in val_list[start:end] if x is not None]

        # Temperature checks
        if is_today:
            current_temp = current_weather.get("temperature")
            if current_temp is not None:
                if current_temp < 12:
                    diagnostics.append({
                        "title": "Dormência/Paralisação",
                        "message": "Temperatura base atingida. Brotação paralisada fisiologicamente.",
                        "type": "danger"
                    })
                elif current_temp < 18:
                    diagnostics.append({
                        "title": "Emergência Lenta",
                        "message": "Solo frio atrasa a brotação e expõe o tolete a fungos. Monitore falhas.",
                        "type": "warning"
                    })
                elif 20 <= current_temp <= 30:
                    diagnostics.append({
                        "title": "Condições Ideais",
                        "message": "Temperatura ótima para atividade enzimática das gemas.",
                        "type": "success"
                    })
        else:
            # Forecast logic
            day_temps = get_hourly_slice("temperature_2m")
            if day_temps:
                avg_temp = sum(day_temps) / len(day_temps)
                if avg_temp < 18:
                        diagnostics.append({
                        "title": "Previsão: Emergência Lenta",
                        "message": "Temperaturas baixas previstas podem atrasar a brotação.",
                        "type": "warning"
                    })

        # Moisture checks
        day_moisture = get_hourly_slice("soil_moisture_0_to_1cm")
        recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)
        
        if recent_moisture is not None and recent_moisture < 0.25:
                diagnostics.append({
                    "title": "Risco de Falha",
                    "message": "Solo superficial seco. Irrigação de salvamento recomendada.",
                    "type": "danger"
                })
        
        return diagnostics

    def analyze_tips(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather, day_index: int, is_today: bool) -> List[Dict[str, str]]:
        tips = []

        def get_hourly_slice(attr):
            val_list = getattr(hourly, attr, None)
            if not val_list: return []
            start = day_index * 24
            end = start + 24
            return [x for x in val_list[start:end] if x is not None]

        day_temps = get_hourly_slice("temperature_2m")
        
        if is_today:
            current_temp = current_weather.get("temperature")
            if current_temp is not None and current_temp < 18:
                    tips.append({
                    "message": "⚠️ Emergência Lenta: Solo frio atrasa a brotação. Monitore falhas.",
                    "type": "warning"
                })
        elif day_temps:
                if (sum(day_temps)/len(day_temps)) < 18:
                    tips.append({
                    "message": "⚠️ Previsão de Frio: Temperaturas baixas podem desacelerar a emergência.",
                    "type": "warning"
                })
        
        day_moisture = get_hourly_slice("soil_moisture_0_to_1cm")
        recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)

        if recent_moisture is not None and recent_moisture < 0.20:
                tips.append({
                    "message": "💧 Risco de Falha: Solo seco. Irrigação de salvamento necessária.",
                    "type": "danger"
                })

        if day_temps and max(day_temps) > 30:
            day_humidity = get_hourly_slice("relativehumidity_2m")
            avg_humidity = sum(day_humidity)/len(day_humidity) if day_humidity else 0
            if avg_humidity > 60: 
                tips.append({
                    "message": "🚀 Condições Ótimas: Calor e umidade favorecem emergência rápida.",
                    "type": "success"
                })
        
        return tips
