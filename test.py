from pyrogram import Client, filters
from pyrogram.types import Message


@Client.on_message(filters.command('t', '.') & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit('<code>TEST</code>')
