import json
from app.states.base import AgentState


class SummarizationState(AgentState):
    """Summarization State: Generates the final user-facing response."""

    def __init__(self):
        super().__init__(
            name="summarizing",
            system_prompt=(
                "You are a summarization assistant. Your task is to generate a final, natural language answer for the user. "
                "CRITICAL INSTRUCTIONS: "
                "1. You MUST ONLY use the information provided in the conversation history, especially from the 'assistant' role. "
                "2. You MUST base your answer ONLY on the text provided in the 'assistant' role. "
                "3. Your response MUST be a simple, natural language sentence. DO NOT output JSON. "
                "The original user request was: '{user_request}'"
            ),
        )

    async def execute(
        self, agent: "StatefulAgent", context: dict = None
    ) -> tuple[str, dict]:
        
        print("Entering to [Summarizing] Status...")

        original_request = next(
            (msg["content"] for msg in agent.memory if msg["role"] == "user"), ""
        )

        formatted_prompt = self.system_prompt.format(user_request=original_request)

        # Remove the duplicate info
        tool_results = []
        seen_results = set()
        for msg in agent.memory:
            if msg["role"] == "assistant":
                if msg["content"] not in seen_results:
                    tool_results.append(msg)
                    seen_results.add(msg["content"])

        messages_for_summary = [
            {"role": "system", "content": formatted_prompt},
            next((msg for msg in agent.memory if msg["role"] == "user"), None),
        ] + tool_results

        messages_for_summary = [msg for msg in messages_for_summary if msg is not None]

        print("--- Sending curated context to summarizer LLM ---")
        for msg in messages_for_summary:
            print(msg)
        print("-------------------------------------------------")
        _, final_answer, _ = await agent.llm.chat(messages_for_summary)

        return "finished", {"final_answer": final_answer}
