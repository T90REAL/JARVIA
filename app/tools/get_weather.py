import asyncio
from base import BaseTool
from base import ToolResult

WEATHER_DB = {
    "Tokyp": {"temperature": "28°C", "condition": "晴"},
    "Shanghai": {"temperature": "31°C", "condition": "多云"},
}


class GetWeatherTool(BaseTool):
    """
    A tool to get today's weather for a given city
    """

    name: str = "get_todays_waether"
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
        print(f"--- 正在执行 GetWeatherTool, 查询城市: {city} ---")

        weather_info = WEATHER_DB.get(city)

        if weather_info:
            return f"{city}的天气是{weather_info['condition']}，气温{weather_info['temperature']}。"
        else:
            raise ValueError(f"找不到城市 '{city}' 的天气信息。")


async def main():
    weather_tool = GetWeatherTool()

    print(weather_tool.to_llm_format)

    res = await weather_tool(city="Shanghai")
    print(f"result = {res}")


if __name__ == "__main__":
    asyncio.run(main())
