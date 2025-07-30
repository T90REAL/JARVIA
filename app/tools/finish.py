from app.tools.base import BaseTool


class FinishTool(BaseTool):
    name: str = "finish_task"
    description: str = "When all tasks have been completed, call this tool to report the final answer to the user and end the process."
    parameters: dict = {
        "type": "object",
        "properties": {
            "final_answer": {
                "type": "string",
                "description": "Final response to the user based on the operations."
            }
        },
        "required": ["final_answer"],
    }

    async def _execute(self, final_answer: str) -> str:
        return final_answer