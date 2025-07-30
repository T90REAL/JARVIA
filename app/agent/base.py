from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Optional, Any, AsyncGenerator

from app.llm.base import BaseLLM
from app.tools.tool_box import ToolBox
from app.states.base import AgentStepResult

class BaseAgent(BaseModel, ABC):
    """
    This is a abstract agent for further expanding.
    """

    name: str = Field(default="Default agent", description="Individual agent.")
    description: Optional[str] = Field(default=None, description="The functionality of this agent.")
    llm: BaseLLM = Field(..., description="The selected large language model (brain).")
    max_steps: int = Field(default=5, description="The max steps that llm is going to loop.")
    memory: list = Field([], description="The memory of the agent.")
    toolbox: ToolBox = Field(default_factory=ToolBox, description="The tools that llm can use.")
    states: dict = Field(..., description="All the states the agent can have")


    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    async def run(self) -> AsyncGenerator[AgentStepResult, None]:
        """
        The method that defines how the agent work
        """
        pass