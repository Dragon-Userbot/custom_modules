from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import with_reply


@Client.on_message(filters.command("msave", prefix) & filters.me)
@with_reply
async def msave(client: Client, message: Message):
    media = message.reply_to_message.media.value

    if not media:
        await message.edit("<b>Media is required</b>")
        return
    await message.delete()

    path = await message.reply_to_message.download(in_memory=True)
    await getattr(client, f"send_{media}")("me", path)


modules_help["mediasaver"] = {
    "msave": "Save self-destructing media and send it to Saved Messages",
}
