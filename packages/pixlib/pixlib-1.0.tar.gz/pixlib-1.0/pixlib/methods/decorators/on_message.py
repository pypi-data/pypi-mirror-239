from typing import Callable

import pixlib
from pixlib.filters import Filter


class OnMessage:
    def on_message(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling new messages.

        This does the same thing as :meth:`~pixlib.Client.add_handler` using the
        :obj:`~pixlib.handlers.MessageHandler`.

        Parameters:
            filters (:obj:`~pixlib.filters`, *optional*):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pixlib.Client):
                self.add_handler(pixlib.handlers.MessageHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pixlib.handlers.MessageHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
