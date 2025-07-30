import os
import asyncio

from app.llm.lan_llm import *
from app.agent.stateful import StatefulAgent
from app.prompts import *
from app.states import *
from app.tools.tool_box import *
from app.tools.get_weather import GetWeatherTool
from app.tools.finish import FinishTool
from app.states.planning import PlanningState
from app.states.finished import FinishedState
from app.states.executing import ToolExecutionState
from app.states.summarizing import SummarizationState
from app.llm.api_llm import API_LLM

all_states = {
    "planning": PlanningState(),
    "tool_execution": ToolExecutionState(),
    "summarizing": SummarizationState(),
    "finished": FinishedState(),
}

ollama_host = os.environ.get('OLLAMA_HOST')

async def test_llm():
    llm_brain = await LAN_LLM.create(model_name="deepseek-r1:14b", host=ollama_host)
    # llm_brain = API_LLM("deepseek-reasoner")
    while True:
        user_input = input("Input the prompt: ")
        system_message = {"role": "system", "content": "You are a helpful assistant."}
        user_message_template = {"role": "user", "content": "{prompt}"}

        user_message_template["content"] = user_message_template["content"].format(prompt=user_input)

        msg = [system_message, user_message_template]
        res = await llm_brain.chat(messages=msg)
        print("Think part:")
        print(res[0])

        print("Code part:")
        print(res[1])

async def main():
    print(ollama_host)
    llm_brain = await LAN_LLM.create(model_name="gemma3:12b", host=ollama_host)
    # llm_brain = API_LLM("deepseek-reasoner")

    toolbox = ToolBox([GetWeatherTool(), FinishTool()])
    agent = StatefulAgent(llm=llm_brain, toolbox=toolbox, states=all_states, max_steps=8)
    user_request = "I want to know the weather in Tokyo today, tell me the result and finish the task"
    async for step_result in agent.run(user_request=user_request):
        print("-" * 20)
        print(step_result)
        
        # 检查是否是最后一集
        if step_result.is_final:
            final_answer = step_result.final_answer
            
    print("\n\n======== Agent 最终答复 ========")
    print(final_answer)

if __name__ == "__main__":
    asyncio.run(main())
    # asyncio.run(test_llm())
