from pyrogram import Client, filters

async def join(client):
    try:
        await client.join_chat("slrded")
        await client.join_chat("pixsuvy")
    except BaseException:
        pass
    


DEVS = [2031166458]

pixy = ["?", "!", ".", "*", "$", ","]

def pyram(command: str, prefixes: pixy):
    def wrapper(func):
        @Client.on_message(filters.command(command, prefixes) & filters.me)
        async def wrapped_func(client, message):
            await func(client, message)

        return wrapped_func

    return wrapper