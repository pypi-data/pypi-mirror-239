from typing import Callable

import pixlib


class OnRawUpdate:
    def on_raw_update(
        self=None,
        group: int = 0
    ) -> Callable:
        """Decorator for handling raw updates.

        This does the same thing as :meth:`~pixlib.Client.add_handler` using the
        :obj:`~pixlib.handlers.RawUpdateHandler`.

        Parameters:
            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pixlib.Client):
                self.add_handler(pixlib.handlers.RawUpdateHandler(func), group)
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pixlib.handlers.RawUpdateHandler(func),
                        group
                    )
                )

            return func

        return decorator
