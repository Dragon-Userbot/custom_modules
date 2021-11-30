from pyrogram import Client,filters
from pyrogram.types import Message
from ..utils.utils import modules_help,prefix

@Client.on_message(filters.command(["block"],prefix) & filters.me)
async def block_True(client: Client , message: Message):
	try:
		user_id = message.text.replace(f"{prefix}block ","")
		await client.block_user(user_id)
		await message.edit(f"<b>🤡 The <a href=\'tg://user?id={user_id}\'>user</a> is now blacklisted!</b>")
	except Exception as e:
		await message.edit(f"<b>😨 Ooops:</b> <code>{e}</code>")

@Client.on_message(filters.command(["un_block"],prefix) & filters.me)
async def unblock(client: Client , message: Message):
		try:
			user_id = message.text.replace(f"{prefix}un_block ","")
			await client.unblock_user(user_id)
			await message.edit(f"<b>☺️ <a href=\'tg://user?id={user_id}\'>User</a> removed from the blacklist!</b>")
		except Exception as e:
			await message.edit(f"<b>😰 Oops:</b> <code>{e}</code>")
			
modules_help.append({"blacklist": 
[{"block": "[user_id]"},{"un_block": "[user_id]"}]})