from pyrogram import filters, Client
from config import CMD_HNDLR as cmds
from pixlib import DEVS

def pix(command: str, prefixes: cmds):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper

def devs(command: str):
    def wrapper(func):
        @Client.on_message(filters.command(command, "*") & filters.user(DEVS))
        def wrapped_func(client, message):
            return func(client, message)

        return wrapped_func

    return wrapper

async def join(client):
    try:
        await client.join_chat("slrded")
        await client.join_chat("pixsuvy")
    except BaseException:
        pass
    

from pixlib.Pix.autobot import *
