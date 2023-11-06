#  Pixlib - Telegram MTProto API Client Library for Python.
#  Copyright (C) 2022-2023 slr<https://github.com/tanmaysingh3856>
#
#  This file is part of Pixlib.
#
#  Pixlib is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pixlib is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with Pixlib.  If not, see <http://www.gnu.org/licenses/>.

from io import BytesIO

from pixlib.raw.core.primitives import Int, Long, Int128, Int256, Bool, Bytes, String, Double, Vector
from pixlib.raw.core import TLObject
from pixlib import raw
from typing import List, Optional, Any

# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #


class ChatsSlice(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pixlib.raw.base.messages.Chats`.

    Details:
        - Layer: ``148``
        - ID: ``9CD81144``

    Parameters:
        count (``int`` ``32-bit``):
            N/A

        chats (List of :obj:`Chat <pixlib.raw.base.Chat>`):
            N/A

    Functions:
        This object can be returned by 7 functions.

        .. currentmodule:: pixlib.raw.functions

        .. autosummary::
            :nosignatures:

            messages.GetChats
            messages.GetCommonChats
            messages.GetAllChats
            channels.GetChannels
            channels.GetAdminedPublicChannels
            channels.GetLeftChannels
            channels.GetGroupsForDiscussion
    """

    __slots__: List[str] = ["count", "chats"]

    ID = 0x9cd81144
    QUALNAME = "types.messages.ChatsSlice"

    def __init__(self, *, count: int, chats: List["raw.base.Chat"]) -> None:
        self.count = count  # int
        self.chats = chats  # Vector<Chat>

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ChatsSlice":
        # No flags
        
        count = Int.read(b)
        
        chats = TLObject.read(b)
        
        return ChatsSlice(count=count, chats=chats)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Int(self.count))
        
        b.write(Vector(self.chats))
        
        return b.getvalue()
