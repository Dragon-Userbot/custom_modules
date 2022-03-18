from pyrogram import Client, filters
from pyrogram.types import Message
from utils.misc import modules_help, requirements_list, prefix
from time import sleep, time
from custom_modules.exceptions import get_gmuted_users, gmute_user, ungmute_user, get_arg, CheckAdmin


@Client.on_message(filters.command("gmute", prefix) & filters.me)
async def gmute(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I gmute?</b>")
            return
    get_user = await client.get_users(user)
    await gmute_user(get_user.id)
    await message.edit(f"<b>Gmuted {get_user.first_name}, LOL!</b>")


@Client.on_message(filters.command("ungmute", prefix) & filters.me)
async def ungmute(client, message):
    reply = message.reply_to_message
    if reply:
        user = reply.from_user["id"]
    else:
        user = get_arg(message)
        if not user:
            await message.edit("<b>Whom should I ungmute?</b>")
            return
    get_user = await client.get_users(user)
    await ungmute_user(get_user.id)
    await message.edit(f"<b>Unmuted {get_user.first_name}, enjoy!</b>")


@Client.on_message(filters.group & filters.incoming)
async def check_and_del(client, message):
    if not message:
        return
    try:
        if not message.from_user.id in (await get_gmuted_users()):
            return
    except AttributeError:
        return
    message_id = message.message_id
    try:
        await client.delete_messages(message.chat.id, message_id)
    except:
        pass  # you don't have delete rights
        
modules_help["gmute"] = {
    "gmute": " global mute of user",
    "ungmute": "unmute user from global ban"
}
