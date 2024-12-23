from collections import Counter
from aiogram.types import Message
from aiogram.filters import BaseFilter


class List_Filter(BaseFilter):

    def __init__(self, list_values: list) -> None:
        self.list_values = list_values

    async def __call__(self, message: Message) -> bool:
        text = message.text if isinstance(message.text, str) else ""
        message_list = text.replace(",", "").split()
        if len(message_list) > len(self.list_values):
            return False

        messages = dict(Counter(message_list))
        is_correct_values = all([message.title() in self.list_values for message in messages.keys()])
        is_correct_count = max(messages.values()) == 1

        return is_correct_values and is_correct_count
