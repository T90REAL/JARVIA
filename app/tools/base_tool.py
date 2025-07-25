"""
一个“好”的 BaseTool 应该具备以下几个特点：

抽象性 (Abstraction): 它应该是一个抽象类，只定义“工具应该长什么样”，而不关心具体“工具做什么”。

描述性 (Descriptiveness): 它必须能清晰地向LLM描述自己的名称、功能和所需参数。

契约性 (Contract): 它必须强制所有继承它的子类都实现一个核心的执行方法。

标准化 (Standardization): 它的输入（参数）和输出（结果）都应该有标准化的格式。

便捷性 (Convenience): 应该让开发者用起来尽可能简单。

异步优先 (Async-First): 鉴于工具很可能涉及网络I/O, 设计上应优先支持 async/await。
"""


from typing import Any, Optional
from pydantic import BaseModel, Field
from abc import ABC, abstractmethod


class BaseTool(BaseModel, ABC):
    name: str
    description: str

    async def __call__(self, **kwargs) -> Any:
        return await self.execute(**kwargs)

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """The implementation of the tool execution."""