import re
import sys
import ollama


class LAN_LLM:
    """
    This is a class for user to select the desired LLM and run it on your own Lan-server
    """

    def __init__(self, model_name: str, host: str):
        """
        Initialize the LLM using Ollama based on the name of the model and the server

        Args:
            model_name (str): The model that is going to be used, such as "deepseek-r1:14b", "qwen3:8b"
            More model details can be found in:
                - https://ollama.com/search
                - https://huggingface.co/models
            host (str): Ollama server ip address, such as "http://192.168.31.100:11434"
                - you can test your service by using `curl ip_address` to check if Ollama is running or not
        """

        print(f"Start connecting to the host: {host}...")
        self.model_name = model_name
        self.host = host
        self.client = ollama.Client(host=self.host)
        self.history = []

        # for model in self.client.list()['models']:
        #     print(model['model'])

        try:
            server_models = [model["model"] for model in self.client.list()["models"]]

            if model_name not in server_models:
                # TODO: Ask user to download manully or hiddenly
                print(
                    f"Your input model '{model_name}' is not in the Server's model list"
                )
            else:
                print(f"Found the mode '{model_name}' on the server!")

        except Exception as e:
            print(f"Can not connect to the host '{host}'. Error : {e}")

            # TODO: I am not sure if it is safe or not?
            sys.exit(1)

    def chat(self, prompt: str) -> tuple:
        """
        This method could communicate with the LLM. Return the Tuple(think part, result part, response time)
        If the selected model is not a reasoning model, the think part would be None
        """

        self.history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = self.client.chat(
                model=self.model_name,
                messages=self.history
            )

            content = response["message"]["content"]
            response_time = response["created_at"]

            self.history.append({"role": "assistant", "content": content})

            if content.find("<think>") == -1:
                # Not a resoning model
                return None, content, response_time
            else:
                think_pattern = r"<think>(.*?)</think>"

                think_part = re.search(think_pattern, content, re.DOTALL).group(1).strip()
                response_part = content.split("</think>")[1]

                return think_part, response_part, response_time
        except Exception as e:
            error_message = f"Some error occur when interacting: {e}"
            print(error_message)
            return error_message


if __name__ == "__main__":
    LAN_HOST = "http://192.168.31.100:11434"

    llm = LAN_LLM(model_name="deepseek-r1:7b", host=LAN_HOST)

    while True:
        user_input = input("Input the prompt: ")
        res = llm.chat(user_input)
        print("Think part:")
        print(res[0])

        print("Code part:")
        print(res[1])
