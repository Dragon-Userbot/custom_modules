from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


@Client.on_message(filters.command("get_my_id", prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit(f"<code>{message.from_user.id}</code>")


@Client.on_message(filters.command("example_send", prefix) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, "<b>This is an example module</b>")


# This adds instructions for your module
modules_help["Тест модуль"] = {
    "get_my_id": "получить свой id",
    "example_edit": "example edit",
}

# modules_help["example"] = { "example_send [text]": "example send" }
#                  |            |              |        |
#                  |            |              |        └─ command description
#           module_name         command_name   └─ optional command arguments
#        (only snake_case)   (only snake_case too)