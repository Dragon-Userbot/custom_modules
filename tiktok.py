import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix


@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client: Client, message: Message):
    if message.reply_to_message:
        link = message.reply_to_message.text
    elif len(message.command) == 2:
        link = message.command[1]
    else:
        return await message.edit(
            "<i>Вы не указали ссылу, ознакомьтесь с докуметацией этого модуля</i>"
        )
    await message.edit("<i>Загрузка...</i>")
    await client.send_message("@ttlessbot", "/start")
    await asyncio.sleep(0.5)
    await client.send_message("@ttlessbot", message.reply_to_message.text)
    await asyncio.sleep(4)
    messages = await client.get_history("@ttlessbot")
    video = messages[1].video.file_id
    await message.delete()
    await client.send_video(message.chat.id, video)


modules_help.append(
    {
        "tiktok": [
            {"tt [link]/[reply]*": "Скачать видео из TikTok и отправить его в чат"}
        ]
    }
)
