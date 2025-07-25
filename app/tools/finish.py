from app.tools.base import BaseTool

class FinishTool(BaseTool):
    nasme: str = "finish_task"
    description: str = "When all tasks have been completed, call this tool to report the final answer to the user and end the process."
    parameters: dict = {
        "type": "object",
        "properties": {"final_answer": {"type": "string", "description": "final result for user"}},
        "required": ["final_answer"],
    }

    async def _execute(self, final_answer) -> str:
        return final_answer