import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from .utils.utils import modules_help, prefix


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client: Client, message: Message):
    await message.edit('<i>Загрузка...</i>')
    if not message.reply_to_message:
        return await message.edit('<i>Эта команда работает только при ответе на сообщение</i>')
    await client.send_message('@ttlessbot', '/start')
    await asyncio.sleep(.5)
    await client.send_message('@ttlessbot', message.reply_to_message.text)
    await asyncio.sleep(4)
    messages = await client.get_history("@ttlessbot")
    video = messages[1].video.file_id
    await message.delete()
    await client.send_video(message.chat.id, video)


modules_help.append(
    {
        "tiktok": [
            {
                "tt [reply]*": "Скачать видео из TikTok и отправить его в чат"
            }
        ]
    }
)
