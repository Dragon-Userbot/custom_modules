from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, prefix

async def download_video(video_url, name):
  requestsVideo = requests.get(video_url, allow_redirects=True)
  open(f"./downloads/video{name}.mp4", "wb").write(requestsVideo.content)

async def sendVideo(message, client, video_url):
  await message.delete()
  chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
  create_hash = ""
  for i in range(10):
    create_hash += random.choice(chars)
  startDownload = time.time()
  snaptik(video_url).get_media()[0].download(f"./downloads/{create_hash}.mp4")
  path = f"./downloads/{create_hash}.mp4"
  endDownload = time.time() - startDownload
  with open(f"./downloads/{create_hash}.mp4", "rb") as file:
    await client.send_video(
      chat_id = message.chat.id,
      video=file,
      caption=f"{round(endDownload, 4)} s"
    )
  os.remove(path)

if not os.path.exists("downloads"):
  os.makedirs("downloads")

@Client.on_message(filters.command("tt", prefix) & filters.me)
async def tiktok(client, message):
  try:
    if message.reply_to_message:
      video_url = message.reply_to_message.text
      await message.edit("Ожидайте")
      await message.edit("Скачиваю видео")
      await sendVideo(message, client, video_url)
    elif len(message.command) > 1:
      video_url = message.command[1]
      await message.edit("Ожидайте")
      await message.edit("Скачиваю видео")
      await sendVideo(message, client, video_url)
    else:
      await message.edit("Реплайните сообщение с ссылкой, или укажите ссылку в аргементе")
  except:
    await message.edit("Ошибка скачки")

modules_help.append(
    {
        "tiktok": [
            {"tt [link]/[reply]*": "Скачать видео из TikTok и отправить его в чат"}
        ]
    }
)
