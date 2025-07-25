from llm.lan_llm import LAN_LLM
from llm.ollama_llm import Ollama_LLM

if __name__ == "__main__":
    LAN_HOST = "http://192.168.31.100:11434"

    # llm = LAN_LLM(model_name="deepseek-r1:7b", host=LAN_HOST)
    llm = Ollama_LLM(model_name="deepseek-r1:7b")

    while True:
        user_input = input("Input the prompt: ")
        res = llm.chat(user_input)
        print("Think part:")
        print(res[0])

        print("Code part:")
        print(res[1])