from typing import Any
from pydantic import BaseModel
from abc import ABC, abstractmethod


class BaseTool(BaseModel, ABC):
    name: str
    description: str

    async def __call__(self, **kwargs) -> Any:
        return await self.execute(**kwargs)

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """The implementation of the tool execution."""
