import asyncio
from typing import Union
from functools import partial

from pixlib import types
from pixlib.filters import Filter


class WaitForMessage:
    async def wait_for_message(
        self,
        chat_id: Union[int, str],
        filters: Filter = None,
        timeout: int = None
    ) -> "types.Message":
        """Wait for message.
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
            filters (:obj:`Filters`):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your callback function.
            timeout (``int``, *optional*):
                Timeout in seconds.
        Returns:
            :obj:`~pixlib.types.Message`: On success, the reply message is returned.
        Raises:
            asyncio.TimeoutError: In case message not received within the timeout.
        Example:
            .. code-block:: python
                # Simple example
                reply_message = app.wait_for_message(chat_id)
                # Example with filter
                reply_message = app.wait_for_message(chat_id, filters=filters.text)
                # Example with timeout
                reply_message = app.wait_for_message(chat_id, timeout=60)
        """

        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        conversation_handler = self.dispatcher.conversation_handler
        future = self.loop.create_future()
        future.add_done_callback(
            partial(
                conversation_handler.delete_waiter,
                chat_id
            )
        )
        waiter = dict(future=future, filters=filters, update_type=types.Message)
        conversation_handler.waiters[chat_id] = waiter
        return await asyncio.wait_for(future, timeout=timeout)
