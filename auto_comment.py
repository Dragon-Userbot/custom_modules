from contextlib import suppress
from pyrogram import Client, filters, ContinuePropagation
from pyrogram.types import Message
from pyrogram.errors import MsgIdInvalid
from ..utils.utils import modules_help, prefix
from ..utils.db import db


@Client.on_message(filters.channel & ~filters.edited)
async def send_comment(client: Client, message: Message):
    auto_comment = db.get("custom.auto_comment", "comment")
    with suppress(MsgIdInvalid):
        if list(auto_comment.keys())[0] == "enable":
            print(message.chat.id)
            msg = await client.get_discussion_message(
                message.chat.id, message.message_id
            )
            await msg.reply(auto_comment["enable"])
    raise ContinuePropagation


@Client.on_message(filters.command(["auto_comment", "ac"], prefix) & filters.me)
async def ping(client: Client, message: Message):
    command = message.command[1]
    if message.command[1] == "enable":
        if len(message.command) == 2:
            return await message.edit("<b>You didn't provide comment text</b>")
        db.set(
            "custom.auto_comment", "comment", {"enable": " ".join(message.command[2:])}
        )
        await message.edit(
            f"<i>Auto comment enabled</i>\n<b>Comment:</b><code> {' '.join(message.command[2:])}</code>"
        )
    elif message.command[1] == "disable":
        db.set("custom.auto_comment", "comment", {"disable": None})
        await message.edit("<i>Auto comment disabled</i>")


modules_help.append(
    {
        "Auto comment": [
            {
                "auto_comment [enable/disable]* [text]": "Enable/disable auto-reply to posts in channels"
            }
        ]
    }
)
