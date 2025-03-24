# import openai
import asyncio
import os
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_gigachat.chat_models import GigaChat


# token = os.getenv("TOKEN_OPENAI")
# token = 'sk-proj-' + token[:3:-1] if token.startswith('gpt:') else token
# openai.api_key = token
chat_token = os.getenv("TOKEN_GIGA_CHAT")

class ChatGPTService:
    def __init__(self):
        self.message_history = []
        self.giga = GigaChat(
            credentials=chat_token,
            verify_ssl_certs=False,
        )

    def set_system_message(self, system_content):
        # self.message_history.append({'role': 'system', 'content': system_content})
        self.message_history.clear()
        self.message_history.append(SystemMessage(system_content))

    # def add_assistant_message(self, assist_content):
    #     self.message_history.append({'role': 'assistant', 'content': assist_content})

    def add_user_message(self, user_content):
        self.message_history.append(HumanMessage(user_content))

    def get_response(self, model='gpt-3.5-turbo', temperature=0.9):
        # response = openai.ChatCompletion.create(
        #     model=model,
        #     messages=self.message_history,
        #     temperature=temperature,
        #     max_tokens=1000,
        # )
        # assistant_reply = response['choices'][0]['message']['content']
        # self.add_assistant_message(assistant_reply)
        res = self.giga.invoke(self.message_history)
        self.message_history.append(res)
        return res.content

