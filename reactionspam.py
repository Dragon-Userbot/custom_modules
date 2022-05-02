import asyncio
from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.types import Message
from utils.misc import modules_help, prefix
from utils.scripts import format_exc

commands = ["vlike", "vdislike", "vheart", "vfire", "vlovely", "vapplaud", "vsmile", "vthinking", "poop", "astonish", "anger", "sad" ]

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vlike(client: Client, message: Message):
	amount = int(message.command[1])
	
	for i in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "👍")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vdislike(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "👎")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vheart(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "❤️")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vfire(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "🔥")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vlovely(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "🥰")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vapplaud(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "👏")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vsmile(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "😁")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vthinking(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "🤔")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vpoop(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "💩")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vastonish(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "😱")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vanger(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "🤬")
		except:
        		pass

@Client.on_message(filters.command(commands, prefix) & filters.me)
async def vsad(client: Client, message: Message):
	amount = int(message.command[1])
	
	for msg in range(amount):
		try:
        		await client.send_reaction(message.chat.id, message.message_id-i, "😢")
		except:
        		pass

modules_help["reactionspam"] = {
	"vlike [amount]": "spam like reaction to a message",
	"vdislike [amount]": "spam dislike reaction to a message",
	"vheart [amount]": "spam heart reaction to a message",
	"vfire [amount]": "spam fire reaction to a message",
	"vlovely [amount]": "spam lovely reaction to a message",
	"vapplaud [amount]": "spam applaud reaction to a message",
	"vsmile [amount]": "spam smile reaction to a message",
	"vthinking [amount]": "spam thinking reaction to a message",
	"vpoop [amount]": "spam poop reaction to a message",
	"vastonish [amount]": "spam astonish reaction to a message",
	"vanger [amount]": "spam anger reaction to a message",
	"vsad [amount]": "spam sad reaction to a message",
	
}
	