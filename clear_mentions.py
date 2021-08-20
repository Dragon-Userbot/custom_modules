from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import Message
from pyrogram.raw import functions, types

from ..utils.utils import modules_help, prefix

@Client.on_message(filters.command(['clear_@'], prefix) & filters.me)
async def solo_clear_handler(c: Client, m: Message):
    await m.delete()
    peer = c.resolve_peer(m.chat.id)
    request = functions.messages.ReadMentions(peer=peer)
    await c.send(request)

@Client.on_message(filters.command(['clear_all_@'], prefix) & filters.me)
async def global_clear_handler(c: Client, m: Message):
    request = functions.messages.GetAllChats(except_ids=[])
    try:
        result = await c.send(request)
    except FloodWait as e:
        await m.edit_text(f'<code>FloodWait received. Wait {e.x} seconds before trying again</code>')
        return
    await m.delete()
    for chat in result.chats:
        if type(chat) is types.Chat:
            peer_id = -chat.id
        elif type(chat) is types.Channel:
            peer_id = int(f'-100{chat.id}')
        peer = await c.resolve_peer(peer_id)
        request = functions.messages.ReadMentions(peer=peer)
        await c.send(request)

modules_help.update({'clear_mentions': '''clear_@ - clears all mentions in chat where was sent, clear_all_@ - clears all mentions in all chats''',
                     'clear_mentions module': 'Clear mentions: clear_@, clear_all_@'})
