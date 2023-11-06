import os
from pyrogram import Client
from Pix import bot1, bot

async def fake_log():
    botlog_chat_id = os.environ.get('BOTLOG_CHATID1')
    if botlog_chat_id:
        return
    
    await bot1.start()
    group_name = 'Pixsuvy BotLog'
    group_description = "Pixsuvy BotLog"
    group_description = 'Botlog group successfully created, please dont leave this group\n\n Pix Pyro'
    group = await bot1.create_supergroup(group_name, group_description)
    with open('.env', 'a') as env_file:
        env_file.write(f'\nBOTLOG_CHATID1={group.id}')

    message_text = 'Grouplog has been successfully activated, please add your bot to this group!'
    await bot1.send_message(group.id, message_text)
    await bot1.stop()


async def izzy_meira(client: bot):
    group_name = "Pixsuvy BotLog"
    async for dialog in client.get_dialogs():
        if dialog.chat.title == group_name:
            return dialog.chat
    return None

async def geezlog(client):
    group_name = "Pixsuvy BotLog"
    group_description = "Pixsuvy BotLog"
    group_message = 'Botlog group successfully created, please dont leave this group\n\n Pix Pyro'
    group = await izzy_meira(client)
    if group == 0:
        await client.create_supergroup(group_name, group_description)
        await client.send_message(group.id, group_message)
        return group
    return None