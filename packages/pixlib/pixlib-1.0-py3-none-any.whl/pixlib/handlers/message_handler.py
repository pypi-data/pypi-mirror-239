from typing import Callable
from .handler import Handler
class MessageHandler(Handler):
    """The Message handler class. Used to handle new messages.
    It is intended to be used with :meth:`~pixlib.Client.add_handler`
    For a nicer way to register this handler, have a look at the
    :meth:`~pixlib.Client.on_message` decorator.
    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Message arrives. It takes *(client, message)*
            as positional arguments (look at the section below for a detailed description).
        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of messages to be passed
            in your callback function.
    Other parameters:
        client (:obj:`~pixlib.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.
        message (:obj:`~pixlib.types.Message`):
            The received message.
    """

    def __init__(self, callback: Callable, filters=None):
        super().__init__(callback, filters)
        self.user_callback = callback
        super().__init__(self.resolve_listener, filters)

    async def resolve_listener(self, client, message, *args):
        listener = client.listening.get(message.chat.id)
        if listener and not listener['future'].done():
            listener['future'].set_result(message)
        else:
            if listener and listener['future'].done():
                client.clear_listener(message.chat.id, listener['future'])
            await self.user_callback(client, message, *args)

    async def check(self, client, update):
        listener = client.listening.get(update.chat.id)

        if listener and not listener['future'].done():
            return await listener['filters'](client, update) if callable(listener['filters']) else True

        return (
            await self.filters(client, update)
            if callable(self.filters)
            else True
        )
