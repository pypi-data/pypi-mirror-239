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


class ExportInvoice(TLObject):  # type: ignore
    """Telegram API function.

    Details:
        - Layer: ``148``
        - ID: ``F91B065``

    Parameters:
        invoice_media (:obj:`InputMedia <pixlib.raw.base.InputMedia>`):
            N/A

    Returns:
        :obj:`payments.ExportedInvoice <pixlib.raw.base.payments.ExportedInvoice>`
    """

    __slots__: List[str] = ["invoice_media"]

    ID = 0xf91b065
    QUALNAME = "functions.payments.ExportInvoice"

    def __init__(self, *, invoice_media: "raw.base.InputMedia") -> None:
        self.invoice_media = invoice_media  # InputMedia

    @staticmethod
    def read(b: BytesIO, *args: Any) -> "ExportInvoice":
        # No flags
        
        invoice_media = TLObject.read(b)
        
        return ExportInvoice(invoice_media=invoice_media)

    def write(self, *args) -> bytes:
        b = BytesIO()
        b.write(Int(self.ID, False))

        # No flags
        
        b.write(self.invoice_media.write())
        
        return b.getvalue()
