from pyrogram import Client, filters
from pyrogram.types import Message
from asyncio import sleep

from ..utils.utils import modules_help, prefix

digits = {
    str(i): el
    for i, el in enumerate(
        ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    )
}


def prettify(val: int) -> str:
    return "".join(digits[i] for i in str(val))


@Client.on_message(filters.command("1000", prefix) & filters.me)
async def ghoul_counter(c: Client, m: Message):
    await m.delete()
    counter = 1000

    message = await c.send_message(m.chat.id, prettify(counter))

    await sleep(1)

    while counter // 7:
        counter -= 7
        await message.edit_text(prettify(counter))
        await sleep(1)

    await message.edit_text("<b>🤡 ГУЛЬ 🤡</b>")


modules_help.append({"1000-7": [{"1000": "counting from 1000 to 0 as a ghoul"}]})
