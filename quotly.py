import asyncio
from asyncio import sleep
import random
import requests
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, prefix



@Client.on_message(filters.command("q", prefix) & filters.me)
async def quotly(client: Client, message: Message):
    if not message.reply_to_message:
        await message.edit("Reply to any users text message")
        return

    await message.edit("<code>Making a Quote</code>")

    await message.reply_to_message.forward("@QuotLyBot")

    is_sticker = False
    progress = 0

    while not is_sticker:
        try:
            await sleep(4)
            msg = await client.get_history("@QuotLyBot", 1)
            print(msg)
            is_sticker = True
        except:
            await sleep(1)

            progress += random.randint(0, 5)

            if progress > 100:
                await message.edit('There was an error')
                return

            try:
                await message.edit("<code>Making a Quote\nProcessing {}%</code>".format(progress))
            except:
                await message.edit("ERROR")

    if msg_id := msg[0]['message_id']:
        await asyncio.gather(
            message.delete(),
            client.forward_messages(message.chat.id, "@QuotLyBot", msg_id)
        )
        
modules_help["quotly"] = {"q": "Reply to any message to make a quote"}
