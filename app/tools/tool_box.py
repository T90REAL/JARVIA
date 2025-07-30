from app.tools.base import BaseTool, ToolResult

class ToolBox:
    def __init__(self, tools: list[BaseTool]):
        self.tools = {tool.name: tool for tool in tools}
        print("The tools:", end=' ')
        for tool in tools:
            print("'" + tool.name + "'", end=', ')
        print("has been enrolled.")
    
    def get_llm_tool_definitions(self) -> list[dict]:
        """
        Generate a tool list that llm can understand
        """
        return [tool.to_llm_format() for tool in self.tools.values()]
    
    async def call(self, tool_name: str, **kwargs) -> ToolResult:
        """
        Calling tools by name
        """
        if tool_name not in self.tools:
            return ToolResult(error=f"Tool {tool_name} does not exist.")
        tool_to_call = self.tools[tool_name]
        return await tool_to_call(**kwargs)
