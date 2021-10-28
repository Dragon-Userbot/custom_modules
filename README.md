<h2>Custom modules</h2>


<p>To add your module to the bot, create a pull request in the <a href='https://github.com/Dragon-Userbot/custom_modules/'>custom_modules</a> repository</p>
<p>Either send the module and its hash to me (<a href='https://t.me/john_phonk'>@john_phonk</a>) details in this <a href='https://t.me/Dragon_Userbot/65'>post</a></p>

```python3
from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, requirements_list

# packages from PyPI
#import example_1
#import example_2


@Client.on_message(filters.command('example_edit', ['.']) & filters.me)
async def example_edit(client: Client, message: Message):
    await message.edit('<code>This is an example module</code>')


@Client.on_message(filters.command('example_send', ['.']) & filters.me)
async def example_send(client: Client, message: Message):
    await client.send_message(message.chat.id, '<b>This is an example module</b>')

# This adds instructions for your module
modules_help.update({'example': '''example_send - example send, example_edit - example edit''',
                     'example module': 'Example_send: example_send, example_edit'})

#'module_name': '''comand_1 - description, comand_2 - description''',
#        │          'module_name module': 'Example_send: example_send, example_edit'
#        │                 │        │
#        │                 │        │
#     module_name(only snake_case)  └─ module (here the word 'module' is required)
#
#If you need to put a COMMA inside the description, then put not a standard sign, but this ->[ ，]

# If your custom module requires packages from PyPI, write the names of the packages in these functions
# requirements_list.append('example_1')
# requirements_list.append('example_2')
# etc
```
