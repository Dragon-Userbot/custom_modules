from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix
import html
import asyncio

@Client.on_message(filters.command('calc', prefix) & filters.me)
async def calc(client: Client, message: Message):
    if len(message.command) > 1:
        args = ' '.join(message.command[1:])
        try:
            result = str(eval(args))

            if len(result) > 4096:
                i = 0
                for x in range(0, len(result), 4096):
                    if i == 0:
                        await message.edit(f'<i>{args}</i><b>=</b><code>{result[x:x+4000]}</code>', parse_mode='HTML')
                    else:
                        await message.reply(f'<code>{result[x:x+4096]}</code>', parse_mode='HTML')
                    i += 1
                    await asyncio.sleep(0.18)
            else:
                await message.edit(f'<i>{args}</i><b>=</b><code>{result}</code>', parse_mode='HTML')
        except Exception as e:
            await message.edit(f'<i>{args}=</i><b>=</b><code>{e}</code>', parse_mode='HTML')


modules_help.update({'calculator': '''calc [expression] - Solve a math problem\n+ – addition\n– – subtraction\n* – multiplication\n/ – division\n** – degree''',
                     'calculator module': 'Calculator: calc'})

