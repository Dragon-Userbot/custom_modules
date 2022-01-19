from pyrogram import Client, filters
from pyrogram.types import Message
import socket
import username
import os
import platform
import time
import psutil
from datetime import datetime
import humanize
import os
import subprocess
from win32api import GetSystemMetrics
from winreg import *
import GPUtil
from ..utils.utils import modules_help, prefix

uptime = psutil.boot_time()
uptime = datetime.fromtimestamp(uptime)
uptime = humanize.precisedelta(uptime)

text = subprocess.getoutput("scoop list")
text = os.linesep.join([s for s in text.splitlines() if s])
package_counter = len(text.strip().split("\n"))
package_counter = int(package_counter) - 1

aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)
aKey = OpenKey(aReg, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
name = QueryValueEx(aKey, 'ProcessorNameString')[0]

gpus = GPUtil.getGPUs()

mem = psutil.virtual_memory()

for gpu in gpus:
  gpuName = gpu.name

def convert_bytes(num):
  for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
    if num < 1024.0:
      return f"{round(num, 2)} {x}"
    num /= 1024.0

sysArchitecture = platform.architecture()[0]

@Client.on_message(filters.command("neofetch", prefix) & filters.me)
async def neofetch(client: Client, message: Message):
  await message.edit(f"""
{username()}@{socket.gethostname()}
———————————————
OS - {platform.system()} {platform.machine()}
Kernel - {platform.version()}
Uptime - {uptime}
Packages - {package_counter}
Resolution - {GetSystemMetrics(0)}x{GetSystemMetrics(1)}
CPU - {name}
GPU - {gpuName}
Memory - {convert_bytes(mem.used)} / {convert_bytes(mem.total)}
Python Version - {platform.python_version()}
Python Compiler - {platform.python_compiler()}
Python Implementation - {platform.python_implementation()}
""")

modules_help.append(
    {"neofetch": [{"neofetch": "View Server/Pc Statistics"}]}
)
