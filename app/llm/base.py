import re
import sys
from abc import ABC, abstractmethod


class BaseLLM(ABC):
    """
    An abstract LLM class
    """

    def __init__(self, model_name: str):
        """
        Initialize the LLM based on the name of the model

        Args:
            model_name (str): The model that is going to be used, such as "deepseek-r1:14b", "qwen3:8b"
            More model details can be found in:
                - https://ollama.com
                - https://huggingface.co/models
        """

        print(f"Start initializing the LLM: {model_name}...")
        self.model_name = model_name
        self.history = []
        self.client = self._create_client()
        self._check_model_exists()

    @abstractmethod
    def _create_client(self):
        """
        An abstract method need to be implemented by different type of LLM.
        """
        pass

    def _check_model_exists(self):
        """
        Check if the model is available on different platform.
        """
        try:
            server_models = [model["model"] for model in self.client.list()["models"]]

            if self.model_name not in server_models:
                # TODO: Ask user to download manully or hiddenly
                raise ValueError(
                    f"Your input model '{self.model_name}' is not on the server's list."
                )
            else:
                print(f"Found the mode '{self.model_name}' on the server!")

        except Exception as e:
            print(f"Can not build the service. Error : {e}")

            # TODO: I am not sure if it is safe or not
            sys.exit(1)

    def chat(self, prompt: str) -> tuple:
        """
        This method could communicate with the LLM. Return the Tuple(think part, result part, response time).
        If the selected model is not a reasoning model, the think part would be None.
        """

        self.history.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        try:
            response = self.client.chat(model=self.model_name, messages=self.history)

            content = response["message"]["content"]
            response_time = response["created_at"]

            self.history.append({"role": "assistant", "content": content})

            if content.find("<think>") == -1:
                # Not a resoning model
                return None, content, response_time
            else:
                think_pattern = r"<think>(.*?)</think>"

                think_part = (
                    re.search(think_pattern, content, re.DOTALL).group(1).strip()
                )
                response_part = content.split("</think>")[1]

                return think_part, response_part, response_time
        except Exception as e:
            error_message = f"Some error occur when interacting: {e}"
            print(error_message)
            return error_message

    def clear_history(self):
        self.history.clear()
