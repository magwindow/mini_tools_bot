from telegram import Message
from telegram.ext.filters import Text

from messages.words import BAD_WORDS


class BadText(Text):
    def filter(self, message: Message) -> bool:
        is_text = super(BadText, self).filter(message)
        if is_text:
            for i in message.text.split(" "):
                if i.lower() in BAD_WORDS:
                    return True
        return False



