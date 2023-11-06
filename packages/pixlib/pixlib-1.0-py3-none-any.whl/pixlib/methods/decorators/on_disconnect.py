from typing import Callable

import pixlib


class OnDisconnect:
    def on_disconnect(self=None) -> Callable:
        """Decorator for handling disconnections.

        This does the same thing as :meth:`~pixlib.Client.add_handler` using the
        :obj:`~pixlib.handlers.DisconnectHandler`.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pixlib.Client):
                self.add_handler(pixlib.handlers.DisconnectHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((pixlib.handlers.DisconnectHandler(func), 0))

            return func

        return decorator
