from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import import_library

wikipedia = import_library("wikipedia")


@Client.on_message(filters.command("wiki", prefix) & filters.me)
async def wiki(client: Client, message: Message):
    lang = message.command[1]
    user_request = " ".join(message.command[2:])
    if user_request == "":
        wikipedia.set_lang("ru")
        user_request = " ".join(message.command[1:])
    try:
        if lang == "en":
            wikipedia.set_lang("en")

        result = wikipedia.summary(user_request)
        await message.edit(
            f"""<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{result}</code>"""
        )

    except Exception as exc:
        await message.edit(
            f"""<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{exc}</code>"""
        )


modules_help.append(
    {"wikipedia": [{"wiki [lang] [request]*": "Search in Russian Wikipedia"}]}
)
