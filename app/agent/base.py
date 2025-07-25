from pydantic import BaseModel, Field
from typing import Optional

class BaseAgent(BaseModel):
    """
    This is a abstract agent for further expanding.
    """

    name: str = Field("agent", description="Individual agent")
    description: Optional[str] = Field(None, description="The functionality of this agent")
    system_prompt: str = Field(None, description="Initial prompt for LLM")
    