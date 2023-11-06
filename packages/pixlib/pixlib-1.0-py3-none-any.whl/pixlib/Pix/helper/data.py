from pyrogram.types import InlineKeyboardButton, WebAppInfo
from Pix import CMD_HNDLR as cmds
class Data:

    text_help_menu = (
        f"**Pix Pyro Help Menu**\n**Prefixes: **{cmds}"
    )
    reopen = [[InlineKeyboardButton("Open Menu", callback_data="reopen")]]
