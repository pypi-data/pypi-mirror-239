from uuid import uuid4

import pixlib
from pixlib import types
from ..object import Object


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~pixlib.types.InlineQueryResultCachedAudio`
    - :obj:`~pixlib.types.InlineQueryResultCachedDocument`
    - :obj:`~pixlib.types.InlineQueryResultCachedAnimation`
    - :obj:`~pixlib.types.InlineQueryResultCachedPhoto`
    - :obj:`~pixlib.types.InlineQueryResultCachedSticker`
    - :obj:`~pixlib.types.InlineQueryResultCachedVideo`
    - :obj:`~pixlib.types.InlineQueryResultCachedVoice`
    - :obj:`~pixlib.types.InlineQueryResultArticle`
    - :obj:`~pixlib.types.InlineQueryResultAudio`
    - :obj:`~pixlib.types.InlineQueryResultContact`
    - :obj:`~pixlib.types.InlineQueryResultDocument`
    - :obj:`~pixlib.types.InlineQueryResultAnimation`
    - :obj:`~pixlib.types.InlineQueryResultLocation`
    - :obj:`~pixlib.types.InlineQueryResultPhoto`
    - :obj:`~pixlib.types.InlineQueryResultVenue`
    - :obj:`~pixlib.types.InlineQueryResultVideo`
    - :obj:`~pixlib.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: "types.InputMessageContent",
        reply_markup: "types.InlineKeyboardMarkup"
    ):
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: "pixlib.Client"):
        pass
