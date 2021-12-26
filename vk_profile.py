from bs4 import BeautifulSoup
from pyrogram import Client, filters
from pyrogram.types import Message
from requests import get

from ..utils.utils import modules_help, prefix

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
}


@Client.on_message(filters.command("vk_profile", prefix) & filters.me)
async def example_edit(client: Client, message: Message):
    text = ""
    await message.edit("<code>Подождите, идёт сканирование профиля...</code>")
    response = get(f"https://vk.com/{message.command[1]}", headers=headers, timeout=3)
    soup = BeautifulSoup(response.text, "html.parser")
    name = f'Имя и фамилия: {soup.find("h1", class_="page_name")}'
    if soup.find("h5", class_="profile_deleted_text"):
        text += f"{name}\n\nСтраница доступна только авторизованным пользователям"
    else:
        text += name
        for item in soup.find_all("div", class_="clear_fix profile_info_row"):
            text += str(item)
    await message.edit(text)


modules_help.append(
    {"vk_profile": [{"vk_profile [link]": "Check open info from VK profile"}]}
)
