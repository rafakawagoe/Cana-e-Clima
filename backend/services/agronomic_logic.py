from typing import List, Dict, Any, Optional
from schemas import DailyWeather, HourlyWeather

class AgronomicLogic:
    def __init__(self):
        pass

    def generate_diagnostics(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather) -> List[Dict[str, List[Dict[str, str]]]]:
        daily_diagnostics = []

        for day_index in range(7):
            diagnostics = {
                "sprouting": [],
                "growth": [],
                "ripening": []
            }
            
            is_today = (day_index == 0)
            
            def get_daily_val(attr, idx):
                val_list = getattr(daily, attr, None)
                return val_list[idx] if val_list and len(val_list) > idx else None
                
            def get_hourly_slice(attr, day_idx):
                val_list = getattr(hourly, attr, None)
                if not val_list: return []
                start = day_idx * 24
                end = start + 24
                return [x for x in val_list[start:end] if x is not None]

            # --- Sprouting Phase ---
            # Temperature checks
            if is_today:
                current_temp = current_weather.get("temperature")
                if current_temp is not None:
                    if current_temp < 12:
                        diagnostics["sprouting"].append({
                            "title": "Dormência/Paralisação",
                            "message": "Temperatura base atingida. Brotação paralisada fisiologicamente.",
                            "type": "danger"
                        })
                    elif current_temp < 18:
                        diagnostics["sprouting"].append({
                            "title": "Emergência Lenta",
                            "message": "Solo frio atrasa a brotação e expõe o tolete a fungos. Monitore falhas.",
                            "type": "warning"
                        })
                    elif 20 <= current_temp <= 30:
                        diagnostics["sprouting"].append({
                            "title": "Condições Ideais",
                            "message": "Temperatura ótima para atividade enzimática das gemas.",
                            "type": "success"
                        })
            else:
                # Forecast logic for Sprouting (using daily min/max or hourly avg)
                day_temps = get_hourly_slice("temperature_2m", day_index)
                if day_temps:
                    avg_temp = sum(day_temps) / len(day_temps)
                    if avg_temp < 18:
                         diagnostics["sprouting"].append({
                            "title": "Previsão: Emergência Lenta",
                            "message": "Temperaturas baixas previstas podem atrasar a brotação.",
                            "type": "warning"
                        })

            # Moisture checks
            day_moisture = get_hourly_slice("soil_moisture_0_to_1cm", day_index)
            recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)
            
            if recent_moisture is not None and recent_moisture < 0.25:
                 diagnostics["sprouting"].append({
                     "title": "Risco de Falha",
                     "message": "Solo superficial seco. Irrigação de salvamento recomendada.",
                     "type": "danger"
                 })

            # --- Growth Phase ---
            day_root_moisture = get_hourly_slice("soil_moisture_27_to_81cm", day_index)
            recent_root_moisture = day_root_moisture[12] if len(day_root_moisture) > 12 else (day_root_moisture[0] if day_root_moisture else None)

            if recent_root_moisture is not None and recent_root_moisture < 0.30:
                diagnostics["growth"].append({
                    "title": "Quebra de TCH",
                    "message": "Déficit hídrico severo. Alongamento de colmos comprometido.",
                    "type": "danger"
                })

            day_temps = get_hourly_slice("temperature_2m", day_index)
            if day_temps and max(day_temps) > 35:
                diagnostics["growth"].append({
                    "title": "Estresse Térmico",
                    "message": "Respiração excessiva consome sacarose. Planta gasta energia para resfriar.",
                    "type": "warning"
                })

            today_rad = get_daily_val("shortwave_radiation_sum", day_index)
            if today_rad is not None and today_rad < 15:
                diagnostics["growth"].append({
                    "title": "Baixa Fotossíntese",
                    "message": "Pouca luz reduz a eficiência C4. Crescimento limitado.",
                    "type": "warning"
                })

            if is_today:
                current_wind = current_weather.get("windspeed")
                if current_wind is not None and current_wind > 10:
                    diagnostics["growth"].append({
                        "title": "Parar Pulverização",
                        "message": "Risco alto de deriva. Suspenda aplicações.",
                        "type": "danger"
                    })
            else:
                 day_winds = get_hourly_slice("windspeed_10m", day_index)
                 if day_winds and max(day_winds) > 15:
                      diagnostics["growth"].append({
                        "title": "Vento Forte Previsto",
                        "message": "Rajadas de vento podem impedir pulverização.",
                        "type": "warning"
                    })

            if recent_root_moisture is not None and recent_root_moisture >= 0.30 and today_rad is not None and today_rad > 20:
                 diagnostics["growth"].append({
                    "title": "Máximo Crescimento",
                    "message": "Taxa fotossintética plena. Aproveite para adubação.",
                    "type": "success"
                })

            # --- Ripening Phase ---
            today_rain = get_daily_val("precipitation_sum", day_index) or 0
            if today_rain > 20:
                diagnostics["ripening"].append({
                    "title": "Queda de ATR",
                    "message": "Chuva na maturação inverte sacarose e dificulta colheita.",
                    "type": "danger"
                })

            if day_temps and recent_moisture is not None:
                if min(day_temps) > 18 and recent_moisture > 0.40:
                    diagnostics["ripening"].append({
                        "title": "Risco de Florescimento",
                        "message": "Noites quentes e umidade induzem isoporização.",
                        "type": "warning"
                    })

            if day_temps and min(day_temps) < 2:
                diagnostics["ripening"].append({
                    "title": "Alerta de Geada",
                    "message": "Risco iminente de morte da gema apical.",
                    "type": "danger"
                })

            if day_temps:
                amplitude = max(day_temps) - min(day_temps)
                if amplitude > 10:
                    diagnostics["ripening"].append({
                        "title": "Pico de Sacarose",
                        "message": "Condições perfeitas para acúmulo de ATR.",
                        "type": "success"
                    })

            # Default Diagnostics
            for phase in diagnostics:
                if not diagnostics[phase]:
                    diagnostics[phase].append({
                        "title": "Condições Normais",
                        "message": "Monitoramento de rotina. Nenhuma condição crítica.",
                        "type": "success"
                    })
            
            daily_diagnostics.append(diagnostics)

        return daily_diagnostics

    def generate_tips(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather) -> List[Dict[str, List[Dict[str, str]]]]:
        daily_tips = []

        for day_index in range(7):
            tips = {
                "sprouting": [],
                "growth": [],
                "ripening": []
            }

            is_today = (day_index == 0)

            def get_daily_val(attr, idx):
                val_list = getattr(daily, attr, None)
                return val_list[idx] if val_list and len(val_list) > idx else None

            def get_hourly_slice(attr, day_idx):
                val_list = getattr(hourly, attr, None)
                if not val_list: return []
                start = day_idx * 24
                end = start + 24
                return [x for x in val_list[start:end] if x is not None]

            # --- Sprouting ---
            day_temps = get_hourly_slice("temperature_2m", day_index)
            
            if is_today:
                current_temp = current_weather.get("temperature")
                if current_temp is not None and current_temp < 18:
                     tips["sprouting"].append({
                        "message": "⚠️ Emergência Lenta: Solo frio atrasa a brotação. Monitore falhas.",
                        "type": "warning"
                    })
            elif day_temps:
                 if (sum(day_temps)/len(day_temps)) < 18:
                      tips["sprouting"].append({
                        "message": "⚠️ Previsão de Frio: Temperaturas baixas podem desacelerar a emergência.",
                        "type": "warning"
                    })
            
            day_moisture = get_hourly_slice("soil_moisture_0_to_1cm", day_index)
            recent_moisture = day_moisture[12] if len(day_moisture) > 12 else (day_moisture[0] if day_moisture else None)

            if recent_moisture is not None and recent_moisture < 0.20:
                 tips["sprouting"].append({
                     "message": "💧 Risco de Falha: Solo seco. Irrigação de salvamento necessária.",
                     "type": "danger"
                 })

            if day_temps and max(day_temps) > 30:
                day_humidity = get_hourly_slice("relativehumidity_2m", day_index)
                avg_humidity = sum(day_humidity)/len(day_humidity) if day_humidity else 0
                if avg_humidity > 60: 
                    tips["sprouting"].append({
                        "message": "🚀 Condições Ótimas: Calor e umidade favorecem emergência rápida.",
                        "type": "success"
                    })

            # --- Growth ---
            if day_temps and max(day_temps) > 35:
                tips["growth"].append({
                    "message": "🔥 Alerta de Respiração: Altas temperaturas consomem sacarose.",
                    "type": "warning"
                })

            today_rad = get_daily_val("shortwave_radiation_sum", day_index)
            if today_rad is not None and today_rad < 15:
                tips["growth"].append({
                    "message": "☁️ Baixa Fotossíntese: Dias nublados reduzem o crescimento.",
                    "type": "info"
                })

            day_root_moisture = get_hourly_slice("soil_moisture_27_to_81cm", day_index)
            recent_root_moisture = day_root_moisture[12] if len(day_root_moisture) > 12 else (day_root_moisture[0] if day_root_moisture else None)

            if recent_root_moisture is not None and recent_root_moisture < 0.30:
                tips["growth"].append({
                    "message": "📉 Perda de TCH: Déficit hídrico gera colmos curtos.",
                    "type": "danger"
                })

            if is_today:
                current_wind = current_weather.get("windspeed")
                if current_wind is not None and current_wind > 10:
                    tips["growth"].append({
                        "message": "🚫 Parar Pulverização: Vento forte. Risco de deriva.",
                        "type": "danger"
                    })
            
            # --- Ripening ---
            today_rain = get_daily_val("precipitation_sum", day_index) or 0
            if today_rain > 30:
                tips["ripening"].append({
                    "message": "🛑 Suspender Colheita: Chuva inverte sacarose e compacta solo.",
                    "type": "danger"
                })

            if day_temps:
                amplitude = max(day_temps) - min(day_temps)
                if amplitude > 10:
                    tips["ripening"].append({
                        "message": "💰 Pico de Açúcar: Amplitude térmica favorece acúmulo de ATR.",
                        "type": "success"
                    })

            if day_temps and min(day_temps) > 18 and recent_moisture is not None and recent_moisture > 0.40:
                 tips["ripening"].append({
                    "message": "🌸 RISCO DE FLORESCIMENTO: Calor e umidade induzem florada.",
                    "type": "warning"
                })

            if day_temps and min(day_temps) < 5:
                tips["ripening"].append({
                    "message": "❄️ Alerta de Geada: Risco de morte da gema apical.",
                    "type": "danger"
                })

            # Default Tips
            for phase in tips:
                if not tips[phase]:
                    tips[phase].append({
                        "message": "✅ Condições Normais: Monitoramento de rotina.",
                        "type": "success"
                    })
            
            daily_tips.append(tips)

        return daily_tips
