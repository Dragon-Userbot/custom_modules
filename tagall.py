import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("tagall", prefix) & filters.me)
async def tagall(client: Client, message: Message):
    await message.delete()
    chat_id = message.chat.id
    string = ""
    limit = 1
    icm = client.iter_chat_members(chat_id)
    async for member in icm:
        tag = member.user.username
        if limit <= 5:
            string += f"@{tag}\n" if tag != None else f"{member.user.mention}\n"
            limit += 1
        else:
            await client.send_message(chat_id, text=string)
            limit = 1
            string = ""
            await asyncio.sleep(2)


modules_help["tagall"] = {
    "tagall": "Tag all members",
}
