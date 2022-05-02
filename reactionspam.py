import asyncio
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

@Client.on_message(filters.command("reactspam", prefix) & filters.me)
async def reactspam(client: Client, message: Message):
	amount = int(message.command[1])
	reaction = " ".join(message.command[2:])
	await message.edit(f"<b>One moment...</b>")
	for i in range(amount):
		if reaction == "👍":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "👍")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "👎":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "👎")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "❤️":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "❤️")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🔥":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🔥")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🥰":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🥰")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "👏":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "👏")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "😁":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "😁")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🤔":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🤔")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🤯":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🤯")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "😱":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "😱")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🤬":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🤬")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "😢":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "😢")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🎉":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🎉")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🤩":
			try:
        			await client.send_reaction(message.chat.id, message.message_id-i, "🤩")

			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "🤮":
			try:
				await client.send_reaction(message.chat.id, message.message_id-i, "🤮")
			except Exception as e:
				return await message.edit(format_exc(e))
		elif reaction == "💩":
			try:
				await client.send_reaction(message.chat.id, message.message_id-i, "💩")
			except Exception as e:
				return await message.edit(format_exc(e))
		else:
			return await message.edit(f"<b>It has to be an emoji...</b>")

	await message.edit(f"<b>Done!</b>")

modules_help["reactionspam"] = {
	"reactspam [amount]* [emoji]*": "spam reactions"

}


