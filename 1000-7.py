from asyncio import sleep

from pyrogram import Client, filters
from pyrogram.types import Message

from ..utils.utils import modules_help, prefix

digits = {
    str(i): el
    for i, el in enumerate(
        ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    )
}


def prettify(val: int) -> str:
    return "".join(digits[i] for i in str(val))


@Client.on_message(filters.command("ghoul", prefix) & filters.me)
async def ghoul_counter(_: Client, m: Message):
    await m.delete()
    counter = 1000
    
    if len(m.command) > 1:
        _ = m.command[1]
        if _.isdigit():
            counter = int(_)
    
    message = await m.reply_text(prettify(counter), quote=False)

    await sleep(1)

    while counter // 7:
        counter -= 7
        await message.edit_text(prettify(counter))
        await sleep(1)

    await message.edit_text("<b>🤡 ГУЛЬ 🤡</b>")


modules_help.append({"1000-7": [{"ghoul {count_from}": "counting from 1000 (or given <code>count_from</code>) to 0 as a ghoul"}]})
