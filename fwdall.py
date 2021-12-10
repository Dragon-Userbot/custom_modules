from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from ..utils import utils
from ..utils.utils import modules_help, prefix
import asyncio

@Client.on_message(filters.command(["fwdall"], prefix) & filters.me)
async def forward(client: Client, message: Message):
    sta = None if len(message.text.split(" ")) < 2 else message.text.split(" ")[1]
    if sta is not None:
        await message.edit("<code>Working...</code>", parse_mode="html")
        try:
            target = await client.get_chat(sta)
        except:
            await message.edit("<code>Unknown target.</code>", parse_mode="html")
            target = None
        if target is not None:
            msgs = []
            async for msg in client.iter_history(message.chat.id, reverse=True):
                msgs.append(msg.message_id)
                if len(msgs) >= 100:
                    try:
                        await client.forward_messages(target.id, message.chat.id, msgs)
                    except FloodWait as e:
                        await asyncio.sleep(e.x)
                        await client.forward_messages(target.id, message.chat.id, msgs)
                    msgs = []
            if len(msgs) > 0:
                try:
                    await client.forward_messages(target.id, message.chat.id, msgs)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await client.forward_messages(target.id, message.chat.id, msgs)
            await message.edit("<code>Done successfully.</code>", parse_mode="html")
    else:
        await message.edit("<code>No target passed.</code>", parse_mode="html")


modules_help.append(
    {
        "fwdall": [
            {
                "fwdall [target]*": "Foraward all messages to defined target [username/chat_id/chat_link]."
            }
        ]
    }
)
