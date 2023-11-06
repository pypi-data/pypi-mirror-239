import pixlib

from ..object import Object

"""- :obj:`~pixlib.types.InputLocationMessageContent`
    - :obj:`~pixlib.types.InputVenueMessageContent`
    - :obj:`~pixlib.types.InputContactMessageContent`"""


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Pyrogram currently supports the following types:

    - :obj:`~pixlib.types.InputTextMessageContent`
    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "pixlib.Client", reply_markup):
        raise NotImplementedError
