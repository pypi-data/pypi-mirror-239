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


class MessageActionSecureValuesSentMe(TLObject):  # type: ignore
    """Telegram API type.

    Constructor of :obj:`~pixlib.raw.base.MessageAction`.

    Details:
        - Layer: ``148``
        - ID: ``1B287353``

    Parameters:
        values (List of :obj:`SecureValue <pixlib.raw.base.SecureValue>`):
            N/A

        credentials (:obj:`SecureCredentialsEncrypted <pixlib.raw.base.SecureCredentialsEncrypted>`):
            N/A

    """

    __slots__: List[str] = ["values", "credentials"]

    ID = 0x1b287353
    QUALNAME = "types.MessageActionSecureValuesSentMe"

    def __init__(self, *, values: List["raw.base.SecureValue"], credentials: "raw.base.SecureCredentialsEncrypted") -> None:
        self.values = values  # Vector<SecureValue>
        self.credentials = credentials  # SecureCredentialsEncrypted

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "MessageActionSecureValuesSentMe":
        # No flags
        
        values = TLObject.read(b)
        
        credentials = TLObject.read(b)
        
        return MessageActionSecureValuesSentMe(values=values, credentials=credentials)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(Vector(self.values))
        
        b.write(self.credentials.write())
        
        return b.getvalue()
