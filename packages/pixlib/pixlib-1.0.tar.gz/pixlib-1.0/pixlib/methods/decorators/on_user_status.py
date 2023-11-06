from typing import Callable

import pixlib
from pixlib.filters import Filter


class OnUserStatus:
    def on_user_status(
        self=None,
        filters=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling user status updates.
        This does the same thing as :meth:`~pixlib.Client.add_handler` using the
        :obj:`~pixlib.handlers.UserStatusHandler`.

        Parameters:
            filters (:obj:`~pixlib.filters`, *optional*):
                Pass one or more filters to allow only a subset of UserStatus updated to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pixlib.Client):
                self.add_handler(pixlib.handlers.UserStatusHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pixlib.handlers.UserStatusHandler(func, self),
                        group if filters is None else filters
                    )
                )

            return func

        return decorator
