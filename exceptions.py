from pyrogram.types import Message, User
from pyrogram import Client
from utils.scripts import import_library
import os

motor = import_library("motor")

import motor.motor_asyncio

    
def paste(TEXT):
      url = "https://del.dog/documents"
      r = requests.post(url, data=str(TEXT)).json()
      url = f"https://del.dog/{r['key']}"
      print(url)
      return url

DATABASE_URL = os.getenv("DATABASE_URL")

cli = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
collection = cli["Dragon"]["gmute"]


async def gmute_user(chat):
    doc = {"_id": "Gmute", "users": [chat]}
    r = await collection.find_one({"_id": "Gmute"})
    if r:
        await collection.update_one({"_id": "Gmute"}, {"$push": {"users": chat}})
    else:
        await collection.insert_one(doc)


async def get_gmuted_users():
    results = await collection.find_one({"_id": "Gmute"})
    if results:
        return results["users"]
    else:
        return []


async def ungmute_user(chat):
    await collection.update_one({"_id": "Gmute"}, {"$pull": {"users": chat}})
    
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])
    
async def CheckAdmin(message: Message):
    """Check if we are an admin."""
    admin = "administrator"
    creator = "creator"
    ranks = [admin, creator]

    SELF = await Client.get_chat_member(
        chat_id=message.chat.id, user_id=message.from_user.id
    )

    if SELF.status not in ranks:
        await message.edit("__I'm not Admin!__")
        sleep(2)
        await message.delete()

    else:
        if SELF.status is not admin or SELF.can_restrict_members:
            return True
        else:
            await message.edit("__No Permissions to restrict Members__")
            sleep(2)
            await message.delete()
