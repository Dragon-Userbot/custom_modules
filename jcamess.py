from utils.scripts import import_library
from utils.misc import modules_help, prefix
from pyrogram.types import Message
from pyrogram import Client, filters





googletrans = import_library("googletrans","googletrans==4.0.0rc1")

from googletrans import Translator

trl = Translator()




@Client.on_message(filters.command(["tr"], prefix) & filters.me)
async def translate(_client, message):
    await message.edit_text("<b>Translating text...</b>")
    if message.reply_to_message and (message.reply_to_message.text or message.reply_to_message.caption):
        if len(message.text.split()) == 1:
            await message.edit("Usage: Reply to a message, then <code>.tr [lang]*</code>")
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
        await message.edit("<b>Translated from</b> <code>{}</code> to <code>{}</code>:\n\n<code>{}</code>".format(detectlang.lang, target, tekstr.text))
    else:
        if len(message.text.split()) <= 2:
            await message.edit("Usage: <code>.tr [lang]* [text]*</code>")
            return
        target = message.text.split(None, 2)[1]
        text = message.text.split(None, 2)[2]
        detectlang = trl.detect(text)
        try:
            tekstr = trl.translate(text, dest=target)
        except ValueError as err:
            await message.edit("Error: <code>{}</code>".format(str(err)))
            return
        await message.edit("<b>Translated from</b> <code>{}</code> to <code>{}</code>:\n\n<code>{}</code>".format(detectlang.lang, target, tekstr.text))
        
@Client.on_message(filters.command(["trdl"], prefix) & filters.me)
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
    "tr": "reply to text with target language code or with language code send message",
    "trdl": "Use when you want to chat with anyone in his language for example you chatting with russian guy and want to say hello do .trdl ru hello it'll edit your message with russian hello and user will be able to understand you and also he can't notice that you using translator"
}
