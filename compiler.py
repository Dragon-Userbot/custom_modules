import pathlib
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.enums import parse_mode
from pyrogram.types import Message

from utils.misc import modules_help, prefix


async def compile(code: str, compiler: str, lang: str):
    tempdir = TemporaryDirectory()
    path = pathlib.Path(tempdir.name)
    with NamedTemporaryFile("w+", suffix=".c", dir=path) as file:
        file.write(code)
        file.seek(0)

        compiled = subprocess.run(
            f"{compiler} -o output {file.name}",
            shell=True,
            capture_output=True,
            text=True,
            cwd=path,
        )

        if compiled.returncode:
            return (
                f"**Language:**\n"
                f"`{lang}`\n\n"
                f"**Code:**\n"
                f"`{code}`\n\n"
                "**Compilation error "
                f"with status code {compiled.returncode}:**\n"
                f"`{compiled.stderr or compiled.stdout}`\n"
            )

        start_time = perf_counter()
        result = subprocess.run(
            "./output", shell=True, capture_output=True, text=True, cwd=path
        )
        stop_time = perf_counter()

        return (
            f"**Language:**\n"
            f"`{lang}`\n\n"
            f"**Code:**\n"
            f"`{code}`\n\n"
            f"**Result with status code {result.returncode}:**\n"
            f"`{result.stderr or result.stdout}`\n\n"
            f"**Completed in {round(stop_time - start_time, 5)}s.**"
        )


@Client.on_message(filters.command(["gcc"], prefix) & filters.me)
async def gcc_runner(_, message: Message):
    await message.edit_text("<i>Executing C code...</i>")
    _, code = message.text.split(maxsplit=1)

    result = await compile(code, "gcc", "C")

    await message.edit_text(result, parse_mode=parse_mode.ParseMode.MARKDOWN)


@Client.on_message(filters.command(["gpp"], prefix) & filters.me)
async def gpp_runner(_, message: Message):
    await message.edit_text("<i>Executing C++ code...</i>")
    _, code = message.text.split(maxsplit=1)

    result = await compile(code, "g++", "C++")

    await message.edit_text(result, parse_mode=parse_mode.ParseMode.MARKDOWN)


modules_help["compiler"] = {
    "gcc [c code]": "Execute C code",
    "gpp [c code]": "Execute C++ code",
}
