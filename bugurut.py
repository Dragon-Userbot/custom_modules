from random import randint

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("bugurut", prefix) & filters.me)
async def telegram(client: Client, message: Message):
    await message.edit(
        f"<b>Рандомный пост из канала:</b> https://t.me/bugurtthread/{randint(21, 35000)}"
    )


modules_help.append({"bugurut": [{"bugurut": "Send random post from bugusrt channel"}]})
