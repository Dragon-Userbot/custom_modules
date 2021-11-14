from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix
import requests
from bs4 import BeautifulSoup

btc = 'https://ru.investing.com/crypto/bitcoin/btc-rub'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}


@Client.on_message(filters.command('course_ru', prefix) & filters.me)
async def convert(client: Client, message: Message):
    try:
        currency = message.command[1]
        link = f'https://ru.investing.com/currencies/{currency}-rub'
        await message.edit('<code>Подождите...</code>')
        if message.command[1] == 'usd':
            name = '1$'
        elif message.command[1] == 'eur':
            name = '1€'
        elif message.command[1] == 'btc':
            name = '1₿'
            link = btc
        else:
            name = currency
        full_page = requests.get(link, headers=headers, timeout=3)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        rub = soup.find('span', id='last_last')
        await message.edit(f'<b>{name} стоит </b><code> {rub} </code><b> rub</b>')
    except:
        await message.edit('<code>ERROR</code>')


modules_help.update({'course-ru': '''course_ru - Используйте для перевода из государственных валют (usd, eur, uah, btc и т.п) в рубль]\n[Не используйте это больше 10-ти раз за минуту''',
    'course_ru module': 'Course_ru: usd, eur, btc и т.п'})
