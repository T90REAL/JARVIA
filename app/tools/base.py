import traceback
from abc import ABC, abstractmethod
from typing import Any, Optional
from pydantic import BaseModel, Field

class ToolResult(BaseModel):
    """
    A standard container to contain the execution result
    """
    result: Any = Field(default=None, description="The output after executing successfully.")
    error: Optional[str] = Field(default=None, description="Saves the error message if executing failed")

    def __str__(self):
        if self.error:
            return f"Error: {self.error}"
        return self.result if self.result is not None else "Tool executed successfully with no output."


class BaseTool(BaseModel, ABC):
	name: str = Field(..., description="The unique name of the tool")
	description: str = Field(..., description="Clear and brief usage description of the tool")
	parameters: Optional[dict] = None

	@abstractmethod
	async def _execute(self, **kwargs) -> Any:
		"""
		An Abstract method. It is the real core logic that every concrete tool must implement.
		It receives parsed parameters and performs tasks.
		"""
		pass

	async def __call__(self, **kwargs) -> ToolResult:
		"""
		A convenient method that allows tool instances to be called directly with built-in unified error handling.
		"""
		try:
			result = await self._execute(**kwargs)
			return ToolResult(result=result)
		except Exception as e:
			error_info = f"Tool '{self.name}' failed with error: {e}"
			print(f"{error_info}\n{traceback.format_exc()}")
			return ToolResult(error=error_info)
		
	def to_llm_format(self) -> dict:
		"""
		Convert the definition of the tool to json format (MCP)
		"""
		return {
			"type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
		}
