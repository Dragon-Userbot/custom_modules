import html
import pathlib
import subprocess
from tempfile import NamedTemporaryFile, TemporaryDirectory
from time import perf_counter

from pyrogram import Client, filters
from pyrogram.types import Message

from utils.misc import modules_help, prefix


def compile(code: str, compiler: str, lang: str):
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
                f"<b>Language:\n</b>"
                f"<code>{lang}</code>\n\n"
                f"<b>Code:</b>\n"
                f"<code>{html.escape(code)}</code>\n\n"
                "<b>Compilation error "
                f"with status code {compiled.returncode}:</b>\n"
                f"<code>{compiled.stderr or compiled.stdout}</code>\n"
            )

        start_time = perf_counter()
        result = subprocess.run(
            "./output", shell=True, capture_output=True, text=True, cwd=path
        )
        stop_time = perf_counter()

        return (
            f"<b>Language:\n</b>"
            f"<code>{lang}</code>\n\n"
            f"<b>Code:</b>\n"
            f"<code>{html.escape(code)}</code>\n\n"
            f"<b>Result with status code {result.returncode}:</b>\n"
            f"<code>{result.stderr or result.stdout}</code>\n\n"
            f"<b>Completed in {round(stop_time - start_time, 5)}s.</b>"
        )


@Client.on_message(filters.command(["gcc"], prefix) & filters.me)
async def gcc_runner(_, message: Message):
    await message.edit_text("<i>Executing C code...</i>")
    _, code = message.text.split(maxsplit=1)

    result = compile(code, "gcc", "C")

    await message.edit_text(result)


@Client.on_message(filters.command(["gpp"], prefix) & filters.me)
async def gpp_runner(_, message: Message):
    await message.edit_text("<i>Executing C++ code...</i>")
    _, code = message.text.split(maxsplit=1)

    result = compile(code, "g++", "C++")

    await message.edit_text(result)


modules_help["compiler"] = {
    "gcc [c code]": "Execute C code",
    "gpp [c code]": "Execute C++ code",
}
