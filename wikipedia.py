from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix
from ..utils.utils import requirements_list

import wikipedia


@Client.on_message(filters.command('wiki', prefix) & filters.me)
async def wiki(client: Client, message: Message):
    lang = message.command[1]
    user_request = ' '.join(message.command[2:])
    if user_request == '':
        wikipedia.set_lang("ru")
        user_request = ' '.join(message.command[1:])
    try:
        if lang == 'en':
            wikipedia.set_lang("en")

        result = wikipedia.summary(user_request)
        await message.edit(f'''<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{result}</code>''')

    except Exception as exc:
        await message.edit(f'''<b>Request:</b>
<code>{user_request}</code>
<b>Result:</b>
<code>{exc}</code>''')


modules_help.update({'wikipedia': '''wiki [request] - Search in Russian Wikipedia,
									 wiki [lang] [request] - Search on the English Wikipedia''',
                     'wikipedia module': 'Wikipedia: wiki'})

requirements_list.append('wikipedia')
