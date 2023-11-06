from typing import Callable

import pixlib
from pixlib.filters import Filter


class OnDeletedMessages:
    def on_deleted_messages(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling deleted messages.

        This does the same thing as :meth:`~pixlib.Client.add_handler` using the
        :obj:`~pixlib.handlers.DeletedMessagesHandler`.

        Parameters:
            filters (:obj:`~pixlib.filters`, *optional*):
                Pass one or more filters to allow only a subset of messages to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pixlib.Client):
                self.add_handler(pixlib.handlers.DeletedMessagesHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pixlib.handlers.DeletedMessagesHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
