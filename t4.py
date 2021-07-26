from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix


@Client.on_message(filters.command('t4', prefix) & filters.me)
async def test2(client: Client, message: Message):
    await message.edit('<code>TEST2</code>')
