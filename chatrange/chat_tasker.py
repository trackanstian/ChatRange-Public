import logging
import sys
from chatrange.open_ai import OpenAIClient, OpenAIMessages
from chatrange.chat_env import BaseConfig
from chatrange.helpers import dprint, conversation, format_string
from chatrange.logger import Logger


class ChatTasker(BaseConfig):
    def __init__(
            self,
            scenario: str,
            phase_name: str = None,
            ):
        super().__init__()
        self.chatconversation = {
            "phase_name": phase_name,
            "phases": [],
            "scenario": scenario
        }
        self.chat_id = []
        self.last_message = None
        pass