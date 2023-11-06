
import pixlib
from pixlib import raw
from pixlib import types


class CreateChannel:
    async def create_channel(
        self: "pixlib.Client",
        title: str,
        description: str = ""
    ) -> "types.Chat":
        """Create a new broadcast channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            title (``str``):
                The channel title.

            description (``str``, *optional*):
                The channel description.

        Returns:
            :obj:`~pixlib.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                await app.create_channel("Channel Title", "Channel Description")
        """
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title,
                about=description,
                broadcast=True
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
