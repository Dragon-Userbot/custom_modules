import os

import ffmpeg
from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix
from utils.scripts import import_library

pytgcalls = import_library("pytgcalls")

from pytgcalls import GroupCallFactory

group_call = None


def init_client(func):
    async def wrapper(client, message):
        global group_call
        if not group_call:
            group_call = GroupCallFactory(client).get_file_group_call()
            group_call.enable_logs_to_console = False

        return await func(client, message)

    return wrapper


async def restart():
    await os.execvp("python3", ["python3", "main.py"])


@Client.on_message(filters.command("play", prefix) & filters.me)
async def start_playout(client, message: Message):
    if not group_call:
        await message.reply_text(
            f"<b>You are not joined [type <code>{prefix}join</code>]</b>"
        )
        return
    if not message.reply_to_message or not message.reply_to_message.audio:
        await message.edit_text("<b>Reply to a message containing audio</b>")
        return
    input_filename = "input.raw"
    await message.edit_text("<code>Downloading...</code>")
    audio_original = await message.reply_to_message.download()
    await message.edit_text("<code>Converting..</code>")
    ffmpeg.input(audio_original).output(
        input_filename, format="s16le", acodec="pcm_s16le", ac=2, ar="48k"
    ).overwrite_output().run()
    os.remove(audio_original)
    await message.edit_text(
        f"<code>Playing</code> <b>{message.reply_to_message.audio.title}</b>..."
    )
    group_call.input_filename = input_filename


@Client.on_message(filters.command("volume", prefix) & filters.me)
@init_client
async def volume(_, message):
    if len(message.command) < 2:
        await message.edit_text("<b>You forgot to pass volume [1-200]</b>")
    await group_call.set_my_volume(message.command[1])
    await message.edit_text(
        f"<b>Your volume is set to</b><code> {message.command[1]}</code>"
    )


@Client.on_message(filters.command("join", prefix) & filters.me)
@init_client
async def start(_, message: Message):
    try:
        await group_call.start(message.chat.id)
        await message.edit_text("<code>Joining successfully!</code>")
    except Exception as e:
        await message.edit_text(
            f"<b>An unexpected error has occurred: <code>{e}</code></b>"
        )


@Client.on_message(filters.command("leave_voice", prefix) & filters.me)
@init_client
async def stop(_, message: Message):
    try:
        await group_call.stop()
        await message.edit_text("<code>Leaving successfully!</code>")
    except Exception as e:
        await message.edit_text(
            f"<b>Аn unexpected error occurred [<code>{e}</code>]\n"
            "The bot will try to exit the voice chat by restarting itself,"
            "the bot will be unavailable for the next 4 seconds</b>"
        )
        restart()


@Client.on_message(filters.command("stop", prefix) & filters.me)
@init_client
async def stop_playout(_, message: Message):
    group_call.stop_playout()
    await message.edit_text("<code>Stoping successfully!</code>")


@Client.on_message(filters.command("vmute", prefix) & filters.me)
@init_client
async def mute(_, message: Message):
    group_call.set_is_mute(True)
    await message.edit_text("<code>Sound off!</code>")


@Client.on_message(filters.command("vunmute", prefix) & filters.me)
@init_client
async def unmute(_, message: Message):
    group_call.set_is_mute(False)
    await message.edit_text("<code>Sound on!</code>")


@Client.on_message(filters.command("pause", prefix) & filters.me)
@init_client
async def pause(_, message: Message):
    group_call.pause_playout()
    await message.edit_text("<code>Paused!</code>")


@Client.on_message(filters.command("resume", prefix) & filters.me)
@init_client
async def resume(_, message: Message):
    group_call.resume_playout()
    await message.edit_text("<code>Resumed!</code>")


modules_help.append(
    {
        "voice_chat": [
            {"play": "Reply to a message containing audio"},
            {"volume [1 – 200]": "Set the volume level from 1 to 200"},
            {"join": "Join the voice chat"},
            {"leave_voice": "Leave voice chat"},
            {"stop": "Stop playback"},
            {"vmute": "Mute the userbot"},
            {"vunmute": "Unmute the userbot"},
            {"pause": "Pause"},
            {"resume": "Resume"},
        ]
    }
)
