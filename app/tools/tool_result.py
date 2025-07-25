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
        return self.output if self.output is not None else "Tool executed successfully with no output."
