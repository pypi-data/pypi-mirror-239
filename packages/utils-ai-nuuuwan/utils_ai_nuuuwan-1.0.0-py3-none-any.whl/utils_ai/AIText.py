import os
import time

import openai
from utils_base import Log

from utils_ai.core.ChatRole import ChatRole
from utils_ai.core.Message import Message

log = Log('AIChat')


class AIText:
    # defaults
    DEFAULT_OPTIONS = dict(
        temperature=0.1,
    )
    DEFAULT_MODEL = 'gpt-4'

    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")  # noqa
        self.messages = []

    def append_message(self, role: ChatRole, content: str):
        self.messages.append(Message(role=role, content=content).todict())

    def send_message(self, message: str) -> str:
        tic = time.perf_counter()
        self.append_message(ChatRole.user, message)
        response = openai.ChatCompletion.create(
            model=AIText.DEFAULT_MODEL,
            messages=self.messages,
            **AIText.DEFAULT_OPTIONS,
        )
        reply = response['choices'][0]['message']['content']

        self.append_message(ChatRole.assistant, reply)
        toc = time.perf_counter()
        log.debug(f'send_message -> {toc - tic:0.4f}s')
        return reply
