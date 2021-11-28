from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix
from ..utils.utils import requirements_list

from random import randint


@Client.on_message(filters.command("bugurut", prefix) & filters.me)
async def telegram(client: Client, message: Message):
    await message.edit(
        f"<b>Рандомный пост из канала:</b> https://t.me/bugurtthread/{randint(21, 35000)}"
    )


modules_help.append({"bugurut": [{"bugurut": "Send random post from bugusrt channel"}]})
