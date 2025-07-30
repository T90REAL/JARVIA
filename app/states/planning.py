import json
from app.states.base import AgentState
from app.prompts.planning import PLANNING_SYSTEM_PROMPT


class PlanningState(AgentState):
    """Planning status: deciding which tool to use next"""

    def __init__(self):
        super().__init__(
            name="planning",
            # system_prompt=PLANNING_SYSTEM_PROMPT
            system_prompt=(
                "You are an expert Planning Agent tasked with solving problems efficiently through structured plans, Your goal is to accomplish the user's task. You have the following tools at your disposal: \n"
                "{tools_json}\n"  # insert all the available tools
                "Based on the user's request and conversation history, choose the most appropriate tool to execute. If the task is completed, use the 'finish_task' tool to reply with the final answer based on the conversation memory.\n"
                "Your answer must be a JSON object in the following format. \n"
                '{{"tool_name": "name of the tool", "arguments": {{"parameter name": "parameter value"}}}}'
            ),
        )

    async def execute(
        self, agent: "StatefulAgent", context: dict = None
    ) -> tuple[str, dict]:
        print("Entering to [Planning] Status...")

        tools_json = json.dumps(
            agent.toolbox.get_llm_tool_definitions(), indent=2, ensure_ascii=False
        )
        formatted_prompt = self.system_prompt.format(tools_json=tools_json)

        # Building messages to LLM
        messages = [{"role": "system", "content": formatted_prompt}] + agent.memory

        print("HERE : ", messages , "endl")

        # Calling LLM for decision making
        _, response_json_str, _ = await agent.llm.chat(messages=messages, format_type="json")

        print("response!!!!!!!", response_json_str)

        tool_call_decision = json.loads(response_json_str)

        # Recording LLM decisions into memory
        agent.memory.append(
            {"role": "assistant", "content": json.dumps(tool_call_decision)}
        )

        tool_name = tool_call_decision.get("tool_name")
        print(tool_call_decision)

        if tool_name == "finish_task":
            return "summarizing", {}
        else:
            # Otherwise, transition to the tool execution state
            return "tool_execution", {"tool_call": tool_call_decision}
