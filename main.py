import os
import asyncio

from app.states import *
from app.prompts import *
from app.llm.api_llm import *
from app.llm.lan_llm import *
from app.tools.finish import *
from app.agent.stateful import *
from app.tools.tool_box import *
from app.states.finished import *
from app.states.planning import *
from app.states.executing import *
from app.tools.get_weather import *
from app.states.summarizing import *

all_states = {
    "planning": PlanningState(),
    "tool_execution": ToolExecutionState(),
    "summarizing": SummarizationState(),
    "finished": FinishedState(),
}

ollama_host = os.environ.get("OLLAMA_HOST")


async def test_llm():
    llm_brain = await LAN_LLM.create(model_name="deepseek-r1:14b", host=ollama_host)
    # llm_brain = API_LLM("deepseek-reasoner")
    while True:
        user_input = input("Input the prompt: ")
        system_message = {"role": "system", "content": "You are a helpful assistant."}
        user_message_template = {"role": "user", "content": "{prompt}"}

        user_message_template["content"] = user_message_template["content"].format(
            prompt=user_input
        )

        msg = [system_message, user_message_template]
        res = await llm_brain.chat(messages=msg)
        print("Think part:")
        print(res[0])

        print("Code part:")
        print(res[1])


async def main():
    llm_brain = await LAN_LLM.create(model_name="deepseek-r1:14b", host=ollama_host)

    toolbox = ToolBox([GetWeatherTool(), FinishTool()])
    agent = StatefulAgent(
        llm=llm_brain, toolbox=toolbox, states=all_states, max_steps=8
    )
    user_request = "I want to know the weather in Shanghai today, tell me the result and finish the task"
    async for step_result in agent.run(user_request=user_request):
        print("-" * 20)
        print(step_result)

        if step_result.is_final:
            final_answer = step_result.final_answer

    print("\n\n======== Agent Final Result ========")
    print(final_answer)


if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(test_llm())
