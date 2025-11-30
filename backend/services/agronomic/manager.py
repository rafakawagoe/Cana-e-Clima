from typing import List, Dict, Any
from schemas import DailyWeather, HourlyWeather
from .sprouting import SproutingAnalyzer
from .growth import GrowthAnalyzer
from .ripening import RipeningAnalyzer

class AgronomicLogic:
    def __init__(self):
        self.sprouting = SproutingAnalyzer()
        self.growth = GrowthAnalyzer()
        self.ripening = RipeningAnalyzer()

    def generate_diagnostics(self, current_weather: Dict[str, Any], daily: DailyWeather, hourly: HourlyWeather) -> List[Dict[str, List[Dict[str, str]]]]:
        daily_diagnostics = []

        for day_index in range(7):
            is_today = (day_index == 0)
            
            diagnostics = {
                "sprouting": self.sprouting.analyze_diagnostics(current_weather, daily, hourly, day_index, is_today),
                "growth": self.growth.analyze_diagnostics(current_weather, daily, hourly, day_index, is_today),
                "ripening": self.ripening.analyze_diagnostics(current_weather, daily, hourly, day_index, is_today)
            }

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
            is_today = (day_index == 0)
            
            tips = {
                "sprouting": self.sprouting.analyze_tips(current_weather, daily, hourly, day_index, is_today),
                "growth": self.growth.analyze_tips(current_weather, daily, hourly, day_index, is_today),
                "ripening": self.ripening.analyze_tips(current_weather, daily, hourly, day_index, is_today)
            }

            # Default Tips
            for phase in tips:
                if not tips[phase]:
                    tips[phase].append({
                        "message": "✅ Condições Normais: Monitoramento de rotina.",
                        "type": "success"
                    })
            
            daily_tips.append(tips)

        return daily_tips
