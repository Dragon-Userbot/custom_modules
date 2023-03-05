from random import randint

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("bugurt", prefix) & filters.me)
async def bugurt(_, message: Message):
    await message.edit(
        f"https://t.me/bugurtthread/{randint(21, 36500)}"
    )
        


modules_help["bugurt"] = {"bugurt": "Send random post from bugurt channel"}
