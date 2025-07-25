class LLM:
    """
    This is a class for user to select the desired LLM
    """
    def __init__(self, model_name: str):
        """
        Initialize the LLM using Ollama based on the name of the model

        Args:
            model_name (str): The model that is going to be used, such as "deepseek-r1:14b", "qwen3:8b"
            More model details can be found in: 
                - https://ollama.com/search
                - https://huggingface.co/models
        """
        self.model_name = model_name
        self.history = []
