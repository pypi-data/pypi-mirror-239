from typing import Optional, List

import pixlib
from pixlib import raw, types
from ..object import Object


class MessageReactions(Object):
    """Contains information about a message reactions.

    Parameters:
        reactions (List of :obj:`~pixlib.types.Reaction`):
            Reactions list.
    """

    def __init__(
        self,
        *,
        client: "pixlib.Client" = None,
        reactions: Optional[List["types.Reaction"]] = None,
    ):
        super().__init__(client)

        self.reactions = reactions

    @staticmethod
    def _parse(
        client: "pixlib.Client",
        message_reactions: Optional["raw.base.MessageReactions"] = None
    ) -> Optional["MessageReactions"]:
        if not message_reactions:
            return None

        return MessageReactions(
            client=client,
            reactions=[types.Reaction._parse_count(client, reaction)
                       for reaction in message_reactions.results]
        )
