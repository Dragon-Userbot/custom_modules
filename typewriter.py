import time
import os
import random
from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, requirements_list, prefix
from pyrogram.errors import FloodWait

# __PLUGIN__ = os.path.basename(__file__.replace(".py", ""))


@Client.on_message(
    filters.command(["type", "typewriter"], prefix) & filters.me
)
async def upload_as_document(c: Client, m: Message):
    text = m.command[1:]
    if not text:
        await m.edit_text("`Input not found`")
        return
    s_time = 0.1
    typing_symbol = "|"
    old_text = ""
    await m.edit_text(typing_symbol)
    time.sleep(s_time)
    for character in text:
        s_t = s_time / random.randint(1, 100)
        old_text += character
        typing_text = old_text + typing_symbol
        try:
            await m.edit_text(typing_text, )
            time.sleep(s_t)
            await m.edit_text(old_text, )
            time.sleep(s_t)
        except FloodWait as ef:
            time.sleep(ef.x)
            LOGGER.info(str(ef))
        return
        
modules_help["typewriter"] = {
    "type": " global mute of user",
    "typewriter": "unmute user from global ban",
}