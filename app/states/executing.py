from app.states.base import AgentState


class ToolExecutionState(AgentState):
    """Tool Execution State: Executes the tool chosen by the PlanningState."""

    def __init__(self):
        # This state is purely procedural and doesn't need its own system prompt for the LLM.
        super().__init__(name="tool_execution", system_prompt="")

    async def execute(
        self, agent: "StatefulAgent", context: dict = None
    ) -> tuple[str, dict]:
        """
        Executes the tool call passed from the context, records the result,
        and transitions back to the planning state.
        """
        print("Entering to [Tool Execution] Status...")

        # 1. Safely get the tool call decision from the context
        tool_call = context.get("tool_call")
        if not tool_call or not isinstance(tool_call, dict):
            # If no valid tool call is provided, transition to an error state
            return "error", {
                "error_message": "No valid tool call provided from the planning state."
            }

        tool_name = tool_call.get("tool_name")
        arguments = tool_call.get("arguments", {})

        if not tool_name:
            return "error", {
                "error_message": "Planning state decided to use a tool but did not provide a name."
            }

        print(f"Executing tool: '{tool_name}' with arguments: {arguments}")

        # 2. Call the tool using the agent's toolbox
        # The toolbox's call method will handle finding and running the tool
        result = await agent.toolbox.call(tool_name, **arguments)

        print(f"Tool '{tool_name}' executed with result: {result}")

        # 3. Record the result of the tool execution into the agent's memory
        # This is crucial for the next planning step, as the LLM will see this result.
        agent.memory.append(
            {
                "role": "assistant",
                "content": str(
                    result
                ),  # Convert result to string to ensure it's serializable
            }
        )

        # 4. Transition back to the planning state to decide the next action
        # The context can be empty because the new information (the tool result)
        # is now in the agent's memory, which the PlanningState will read.
        return "planning", {}
