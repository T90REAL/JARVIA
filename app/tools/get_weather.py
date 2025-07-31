import asyncio

from app.tools.base import BaseTool
from app.tools.base import ToolResult

WEATHER_DB = {
    "Tokyo": {"temperature": "28°C", "condition": "Sunny"},
    "Shanghai": {"temperature": "31°C", "condition": "Cloudy"},
}


class GetWeatherTool(BaseTool):
    """
    A tool to get today's weather for a given city
    """

    name: str = "get_todays_weather"
    description: str = "Get today's weather for the specified city."
    parameters: dict = {
        "type": "object",
        "properties": {
            "city": {
                "type": "string",
                "description": "The name of the city where you want to check the weather, e.g., 'Tokyo' or 'Shanghai'.",
            }
        },
        "required": ["city"],
    }

    async def _execute(self, city: str) -> str:
        """
        Get the weather based on the given city
        """

        # TODO: Make a display class or method later
        print(f"--- Running 'GetWeatherTool', Search weather for city: {city} ---")

        weather_info = WEATHER_DB.get(city)

        if weather_info:
            return f"{city}'s weather is {weather_info['condition']} and temperature is {weather_info['temperature']}."
        else:
            raise ValueError(f"Can not find the '{city}' weather.")
