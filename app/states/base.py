from typing import Any, Optional
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field

"""
State workflow:
[Initialize] -> [planning] -> [tool execution] -> [result evaluating] -> (back to planning) -> [finish or fail]
"""

class AgentState(ABC):
    """Abstract base class for states, defining the “contract” for all states."""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt

    @abstractmethod
    async def execute(self, agent: 'StatefulAgent', context: dict = None) -> tuple[str, dict]:
        """
        Execute the core logic of the current state.
        
        Args:
            agent: Current used Agent
            context: Data passed from the previous state.

        Returns:
            A tuple (next_state_name, new_context) that tells the Agent which state to enter next and what data to pass.
        """
        pass

class AgentStepResult(BaseModel):
    """
    A standardized container for real-time “reporting” on the status and results of each step in the Agent's execution.
    """
    current_state: str = Field(..., description="The state in which the Agent is executing this step.")
    tool_name: Optional[str] = Field(default=None, description="Name of the tool called in this step.")
    tool_input: Optional[dict] = Field(default=None, description="Parameters passed to the tool.")
    tool_output: Optional[str] = Field(default=None, description="Output returned by the tool after execution.")
    is_final: bool = Field(default=False, description="Check if it is the final step.")
    final_answer: Optional[str] = Field(default=None, description="If it is the final step, this should be the answer.")

    def __str__(self):
        if self.is_final:
            return f"✅ [State: {self.current_state}] Final answer: {self.final_answer}"
        
        log = f"🔄 [State: {self.current_state}]"
        if self.tool_name:
            log += f"\n  - Action: tool_to_use: '{self.tool_name}'"
            log += f"\n  - Input: {self.tool_input}"
        if self.tool_output:
            log += f"\n  - Result: {self.tool_output}"
        
        return log