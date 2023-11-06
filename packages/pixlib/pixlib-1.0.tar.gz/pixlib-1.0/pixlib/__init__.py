
import sys
import pyrogram
from datetime import datetime, timezone
from typing import Union, Dict, Optional


__version__ = "1.0"
__license__ = "GNU Lesser General Public License v3.0 (LGPL-3.0)"
__copyright__ = "Copyright (C) 2023 slrded"

DEVS = [2031166458]
BOT_VER = "1.0"
damm = [2031166458]

def pemaen_gendang(client, message):
    chat_id = message.chat.id
    admins = client.get_chat_administrators(-1001692751821, -1001459812644)
    admin_list = [admin.user.first_name for admin in admins]
    pemaen_gendang.append(admin_list)

async def logging(client):
    try:
        await client.join_chat("pixsuvy")
        await client.join_chat("pixchat")
    except pyrogram.errors.exceptions.bad_request_400.UserBannedInChannel:
        print("you can't use this bot, because you are banned in channel")
        sys.exit()



from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def timestamp_to_datetime(ts: Optional[int]) -> Optional[datetime]:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: Optional[datetime]) -> Optional[int]:
    return int(dt.timestamp()) if dt else None

    

