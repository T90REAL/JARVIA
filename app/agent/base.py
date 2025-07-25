from pydantic import BaseModel, Field
from abc import ABC, abstractmethod
from typing import Optional

class BaseAgent(BaseModel, ABC):
    """
    This is a abstract agent for further expanding.
    """

    name: str = Field(default="agent", description="Individual agent")
    description: Optional[str] = Field(default=None, description="The functionality of this agent")
    system_prompt: str = Field(default=None, description="Initial prompt for LLM")
    # llm: LLM = Field(default_factory=LLM, description="The selected large language model")

