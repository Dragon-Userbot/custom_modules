import asyncio

from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix

@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client: Client, message: Message):
    try:
        if message.reply_to_message:
            link = message.reply_to_message.text
        elif len(message.command) == 2:
            link = message.command[1]
        else:
            return await message.edit(
                "<i>Вы не указали ссылку, ознакомьтесь с документацией этого модуля</i>"
            )
        await message.edit("<i>Загрузка...</i>")
        await client.send_message("@downloader_tiktok_bot", link)
        await asyncio.sleep(3)
        messages = await client.get_history("@downloader_tiktok_bot")
        video = messages[0].video.file_id
        await message.delete()
        await client.send_video(message.chat.id, video)
        await client.send(functions.messages.DeleteHistory(peer=await client.resolve_peer("@downloader_tiktok_bot"), max_id=0, revoke=True))
    except AttributeError:
        return await msg.edit(
            "<i>Произошла ошибка при скачивании, попробуйте снова!</i>"
        )


modules_help.append(
    {
        "tiktok": [
            {"tt [link]/[reply]*": "Скачать видео из TikTok и отправить его в чат"}
        ]
    }
)
