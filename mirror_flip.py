from pyrogram import Client, filters
from pyrogram.types import Message
from .utils.utils import modules_help, prefix
from PIL import Image, ImageOps
from io import BytesIO
from asyncio import sleep
import os

async def make(client, message, o):
    reply = message.reply_to_message
    s = None

    if reply.photo or reply.sticker:
        if reply.photo:
            donwloads = await client.download_media(reply.photo.file_id)
        elif reply.sticker:
            donwloads = await client.download_media(reply.sticker.file_id)

        f = open(f"{donwloads}", "rb")

        img = Image.open(BytesIO(f.read()))

        await message.delete()
        w, h = img.size
        if o in [1, 2]:
            if o == 2:
                img = ImageOps.mirror(img)
            part = img.crop([0, 0, w//2, h])
            img = ImageOps.mirror(img)
        else:
            if o == 4:
                img = ImageOps.flip(img)
            part = img.crop([0, 0, w, h//2])
            img = ImageOps.flip(img)
        img.paste(part, (0, 0))
        out = BytesIO()
        out.name = "x.webp" if reply.sticker else "x.png"
        img.save(out)
        out.seek(0)
        if reply.photo:
            return await reply.reply_photo(photo=out)
        elif reply.sticker:
            return await reply.reply_sticker(sticker=out)

        os.remove(donwloads)

    return await message.edit("<b>Need to answer the photo/sticker</b>")

@Client.on_message(filters.command('ll', prefix) & filters.me)
async def mirror_flip(client: Client, message: Message):
    await message.edit('<code>Processing...</code>')
    if len(message.command) > 1:
        param = message.command[1]
        
    else:
        param = 1
    await make(client, message, param)


modules_help.update({'mirror_flip': '''ll - [number(1-4)] Creates a mirrored image/sticker reflection depends on the number''',
                      'mirror_flip module': 'Mirror_flip: ll'})
