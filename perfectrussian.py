from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix

import random


@Client.on_message(filters.command("prus", prefix) & filters.me)
async def prussian_cmd(_, message: Message):
    words = [
        "сука",
        "нахуй",
        "блять",
        "блядь",
        "пиздец",
        "еблан",
        "уебан",
        "уебок",
        "пизда",
        "очко",
        "хуй",
    ]
    splitted = message.text.split()
    
    for i in range(0, len(splitted), random.randint(2, 3)):
        for j in range(1, 2):
            splitted.insert(i, random.choice(words))

    await message.edit(" ".join(splitted))


modules_help["perfectrussian"] = {
    "prus": "translate your message into perfect 🇷🇺Russian",
}
