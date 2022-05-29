from utils.scripts import import_library
from utils.misc import modules_help, prefix
from pyrogram.types import Message
from pyrogram import Client, filters


googletrans = import_library("googletrans", "googletrans==4.0.0rc1")

from googletrans import Translator

trl = Translator()


@Client.on_message(filters.command(["trans"], prefix) & filters.me)
async def translate(_client, message):
    await message.edit_text("<b>Translating text...</b>")
    if message.reply_to_message and (
        message.reply_to_message.text or message.reply_to_message.caption
    ):
        if len(message.text.split()) == 1:
            await message.edit(
                f"<b>Usage: Reply to a message, then <code>{prefix}trans [lang]*</code></b>"
            )
            return
        target = message.text.split()[1]
        if message.reply_to_message.text:
            text = message.reply_to_message.text
        else:
            text = message.reply_to_message.caption
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: <code>{}</code>".format(str(err)))
            return
        await message.edit(
            "<b>Translated from <code>{}</code> to <code>{}</code></b>:\n\n<code>{}</code>".format(
                detectlang.lang, target, tekstr.text
            )
        )
    else:
        if len(message.text.split()) <= 2:
            await message.edit("<b>Usage: <code>.tr [lang]* [text]*</code></b>")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: <code>{}</code>".format(str(err)))
            return
        await message.edit(
            "<b>Translated from <code>{}</code> to <code>{}</code></b>:\n\n<code>{}</code>".format(
                detectlang.lang, target, tekstr.text
            )
        )


@Client.on_message(filters.command(["transdl", "trdl"], prefix) & filters.me)
async def translatedl(_client, message):
    dtarget = message.text.split(None, 2)[1]
    dtext = message.text.split(None, 2)[2]
    ddetectlang = trl.detect(dtext)
    try:
        dtekstr = trl.translate(dtext, dest=dtarget)
    except ValueError as err:
        await message.edit("Error: <code>{}</code>".format(str(err)))
        return
    await message.edit("{}".format(dtekstr.text))


modules_help["translator"] = {
    "trans": "[lang]* [text/reply]* translate message",
    "transdl": f"[lang]* [your text]* short variant of {prefix}trans",
}
