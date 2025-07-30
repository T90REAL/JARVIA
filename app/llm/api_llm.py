import os
import json
import asyncio
from typing import Optional

import openai
from openai import AsyncOpenAI

from app.llm.base import BaseLLM

class API_LLM(BaseLLM):
    """ """

    def __init__(self, model_name: str):
        super().__init__(model_name=model_name)

    def _create_client(self):
        """ """
        print("正在创建OpenAI API异步客户端...")
        # 客户端会自动从环境变量 OPENAI_API_KEY 读取密钥
        try:
            client = AsyncOpenAI(
            )
            return client
        except openai.AuthenticationError as e:
            print(
                "OpenAI API密钥验证失败！请检查您的环境变量 'OPENAI_API_KEY' 是否已正确设置。"
            )
            raise e

    async def chat(self, messages: list, format_type: Optional[str] = None) -> tuple:
        """
        【异步】通过OpenAI API与LLM通信。

        Args:
            messages (list): 发送给模型的完整消息列表。
            format_type (Optional[str], optional): 如果为 "json"，则强制模型返回JSON。

        Returns:
            tuple: (content, response_time)。
        """
        try:
            chat_options = {
                "model": self.model_name,
                "messages": messages,
            }

            if format_type == "json":
                # OpenAI API需要这样来指定JSON模式
                chat_options["response_format"] = {"type": "json_object"}

            response = await self.client.chat.completions.create(**chat_options)

            content = response.choices[0].message.content
            # OpenAI的响应中没有直接的created_at，但我们可以用完成时间戳
            response_time = response.created

            return "", content, response_time

        except openai.APIError as e:
            error_message = f"OpenAI API返回错误: {e}"
            print(error_message)
            if format_type == "json":
                return f'{{"error": "{error_message}"}}', None
            else:
                return "", error_message, None