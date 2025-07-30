from app.states.base import AgentState


class FinishedState(AgentState):
    """Finished status: End workflow"""

    def __init__(self):
        super().__init__(name="finished", system_prompt="")

    async def execute(
        self, agent: "StatefulAgent", context: dict = None
    ) -> tuple[str, dict]:
        print("Entering to [Finished] Status...")
        final_answer = context.get("final_answer", "Task is done.")
        return "finished", {"final_answer": final_answer}


# class ErrorState(AgentState):
#     """Error status: handling errors in execution"""
#     def __init__(self):
#         super().__init__(name="error", system_prompt="")

#     async def execute(self, agent: 'StatefulAgent', context: dict = None) -> tuple[str, dict]:
#         error_message = context.get("error_message", "Unknown error occurs")
#         print(f"Entering to [Error] Status: {error_message}")
#         return "finished", {"final_answer": f"任务因错误而终止: {error_message}"}
