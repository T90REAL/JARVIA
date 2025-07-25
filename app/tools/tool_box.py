from base import BaseTool, ToolResult

class ToolBox:
    def __init__(self, tools: list[BaseTool]):
        self.tools = {tool.name for tool in tools}
    
    def get_llm_tool_definitions(self) -> list[dict]:
        """
        Generate a tool list that llm can understand
        """
        # return [tool.def_to_json for tool in self.tools]
