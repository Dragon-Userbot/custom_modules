import random
import asyncio

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions.flood_420 import FloodWait
from utils.misc import modules_help, prefix

R = "❤️"
W = "🤍"

heart_list = [
    W * 9,
    W * 2 + R * 2 + W + R * 2 + W * 2,
    W + R * 7 + W,
    W + R * 7 + W,
    W + R * 7 + W,
    W * 2 + R * 5 + W * 2,
    W * 3 + R * 3 + W * 3,
    W * 4 + R + W * 4,
    W * 9,
]
joined_heart = "\n".join(heart_list)

heartlet_len = joined_heart.count(R)

SLEEP = 0.1


async def _wrap_edit(message: Message, text: str):
    """Floodwait-safe utility wrapper for edit"""
    try:
        await message.edit(text)
    except FloodWait as fl:
        await asyncio.sleep(fl.x)


async def phase1(message: Message):
    """Big scroll"""
    BIG_SCROLL = "🧡💛💚💙💜🖤🤎"
    await _wrap_edit(message, joined_heart)
    for heart in BIG_SCROLL:
        await _wrap_edit(message, joined_heart.replace(R, heart))
        await asyncio.sleep(SLEEP)


async def phase2(message: Message):
    """Per-heart randomiser"""
    ALL = ["❤️"] + list("🧡💛💚💙💜🤎🖤")  # don't include white heart

    format_heart = joined_heart.replace(R, "{}")
    for _ in range(5):
        heart = format_heart.format(*random.choices(ALL, k=heartlet_len))
        await _wrap_edit(message, heart)
        await asyncio.sleep(SLEEP)


async def phase3(message: Message):
    """Fill up heartlet matrix"""
    await _wrap_edit(message, joined_heart)
    await asyncio.sleep(SLEEP * 2)
    repl = joined_heart
    for _ in range(joined_heart.count(W)):
        repl = repl.replace(W, R, 1)
        await _wrap_edit(message, repl)
        await asyncio.sleep(SLEEP)


async def phase4(message: Message):
    """Matrix shrinking"""
    for i in range(7, 0, -1):
        heart_matrix = "\n".join([R * i] * i)
        await _wrap_edit(message, heart_matrix)
        await asyncio.sleep(SLEEP)


@Client.on_message(filters.command("hearts", prefix) & filters.me)
async def hearts(client: Client, message: Message):
    await phase1(message)
    await phase2(message)
    await phase3(message)
    await phase4(message)
    await asyncio.sleep(SLEEP * 3)

    final_caption = " ".join(message.command[1:])
    if not final_caption:
        final_caption = "💕 by @arte_m_etra"
    await message.edit(final_caption)


modules_help["hearts"] = {
    "hearts": "Heart animation. May cause floodwaits, use at your own risk!"
}
