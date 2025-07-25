"""
一个“好”的 BaseTool 应该具备以下几个特点：

抽象性 (Abstraction): 它应该是一个抽象类，只定义“工具应该长什么样”，而不关心具体“工具做什么”。

描述性 (Descriptiveness): 它必须能清晰地向LLM描述自己的名称、功能和所需参数。

契约性 (Contract): 它必须强制所有继承它的子类都实现一个核心的执行方法。

标准化 (Standardization): 它的输入（参数）和输出（结果）都应该有标准化的格式。

便捷性 (Convenience): 应该让开发者用起来尽可能简单。

异步优先 (Async-First): 鉴于工具很可能涉及网络I/O, 设计上应优先支持 async/await。
"""

import traceback
from typing import Any
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from tools.tool_result import ToolResult


class BaseTool(BaseModel, ABC):
	name: str = Field(..., description="The unique name of the tool")
	description: str = Field(..., description="Clear and brief usage description of the tool")
	parameters: dict = Field(default_factory=dict, description="JSON Schema definition of the parameters required by the tool",)

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
			return ToolResult(output=result)
		except Exception as e:
			error_info = f"Tool '{self.name}' failed with error: {e}"
			print(f"{error_info}\n{traceback.format_exc()}")
			return ToolResult(error=error_info)
		
	def def_to_json(self) -> dict:
		"""
		Convert the defnition of the tool to json format (MCP)
		"""
		return {
			"type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
		}