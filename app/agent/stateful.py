from typing import AsyncGenerator, Optional
from app.agent.base import BaseAgent
from app.tools.tool_box import ToolBox
from app.states.base import AgentState
from app.states.planning import PlanningState
from app.states.finished import FinishedState
from app.states.base import AgentStepResult


class StatefulAgent(BaseAgent):
    current_state: Optional[AgentState] = None

    def __init__(self, llm, toolbox: ToolBox, states: dict, max_steps: int = 5):
        super().__init__(
            name="StatefulAgent",
            llm=llm,
            max_steps=max_steps,
            memory=[],
            toolbox=toolbox,
            states=states,  # Register all the possible states
        )
        self.current_state = self.states["planning"] # Initial state is planning

    async def run(self, user_request: str) -> AsyncGenerator[AgentStepResult, None]:
        """
        Streams the Agent's think-act loop as an asynchronous generator.
        Each step yields an AgentStepResult object.
        """
        self.memory.append({"role": "user", "content": user_request})
        step_count = 0
        context = {}

        while step_count < self.max_steps:
            step_count += 1

            # Record current state
            state_before_execution = self.current_state.name

            # Execute
            next_state_name, context = await self.current_state.execute(self, context)

            # print(context)
            # print(context.get("tool_call", {}).get("tool_name"))
            # print(context.get("tool_call", {}).get("arguments"))
            # print("??", self.memory[-1]["content"])

            # --- Yield current result ---
            step_result = AgentStepResult(
                current_state=state_before_execution,
                tool_name=context.get("tool_call", {}).get("tool_name"),
                tool_input=context.get("tool_call", {}).get("arguments"),
                tool_output=(
                    self.memory[-1]["content"]
                    if self.memory and self.memory[-1]["role"] == "tool"
                    else None
                ),
            )

            yield step_result
            # -----------------------------------

            # Break if it is the final/error step
            if next_state_name in ["finished", "error"]:
                self.current_state = self.states[next_state_name]
                break

            # Move to the next state
            self.current_state = self.states.get(next_state_name)

            if not self.current_state:
                final_error_result = AgentStepResult(
                    current_state="error",
                    is_final=True,
                    final_answer=f"Error: Try to move the an unknown state: '{next_state_name}'",
                )
                yield final_error_result
                return

        # Get the final answer
        _, final_context = await self.current_state.execute(self, context)
        final_answer = final_context.get("final_answer")

        # Yield the final answer
        final_step_result = AgentStepResult(
            current_state=self.current_state.name,
            is_final=True,
            final_answer=final_answer,
        )
        yield final_step_result
