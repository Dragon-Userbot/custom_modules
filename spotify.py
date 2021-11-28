from pyrogram import Client, filters
from pyrogram.types import Message
from ..utils.utils import modules_help, requirements_list, prefix

from math import ceil
import json
import datetime
import asyncio
import os

try:
    import spotipy
except:
    os.system("pip3 install spotipy")
    os.system("python3 main.py")

modules_help.append(
    {
        "spotify": [
            {"auth": "First auth step"},
            {"codeauth": "Second auth step"},
            {"now": "Display now playing track"},
            {"repeat": "Set track on-repeat"},
            {"derepeat": "Set track out from repeat"},
            {"next": "Turn on next track"},
            {"back": "Turn on previous track"},
            {"restr": "Restart currently playing track from start"},
            {"liketr": "Like current playing track"},
            {"pausetr": "Pause current playing track"},
            {"unpausetr": "Play currently paused track "},
        ]
    }
)
requirements_list.append("spotipy")

client_id = "e0708753ab60499c89ce263de9b4f57a"
client_secret = "80c927166c664ee98a43a2c0e2981b4a"
scope = (
    "user-read-playback-state playlist-read-private playlist-read-collaborative"
    " app-remote-control user-modify-playback-state user-library-modify"
    " user-library-read"
)
sp_auth = spotipy.oauth2.SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="https://fuccsoc.com/",
    scope=scope,
)


def get_db():
    try:
        with open("spotify.json") as dbf:
            db = json.load(dbf)
    except:
        f = open("spotify.json", "w")
        f.write("{}")
        f.close()
        return {}
    return db


def write_db(ttw):
    with open("spotify.json", "w") as dbf:
        json.dump(ttw, dbf)


async def check_token():
    db = get_db()
    if db.get("acs_tkn") != None:
        if db.get("LastChange") != None:
            ttc = datetime.datetime.strptime(
                db.get("LastChange"), "%Y-%m-%dT%H:%M:%S.%f"
            ) + datetime.timedelta(minutes=45)
            crnt = datetime.datetime.now()
            if ttc < crnt:
                db["acs_tkn"] = sp_auth.refresh_access_token(
                    db.get("acs_tkn")["refresh_token"]
                )
                db["LastChange"] = crnt.isoformat()
                write_db(db)
        else:
            crnt = datetime.datetime.now()
            db["acs_tkn"] = sp_auth.refresh_access_token(
                db.get("acs_tkn")["refresh_token"]
            )
            db["LastChange"] = crnt.isoformat()
    write_db(db)


async def check_token_loop():
    while True:
        await check_token()
        await asyncio.sleep(3000)


loop = asyncio.get_event_loop()
loop.create_task(check_token_loop())


@Client.on_message(filters.command("auth", prefix) & filters.me)
async def auth(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") != None:
        await message.edit("⚠️Вы уже авторизованы")
    else:
        sp_auth.get_authorize_url()
        await message.edit(
            f'<a href="{sp_auth.get_authorize_url()}">Перейдите по этой ссылке</a>,'
            " подтвердите доступ, затем скопируйте адрес редиректа и выполните"
            " <code>.codeauth [адрес редедиректа]</code>"
        )


@Client.on_message(filters.command("codeauth", prefix) & filters.me)
async def codeauth(client: Client, message: Message):
    try:
        db = get_db()
        url = message.text.split(" ")[1]
        code = sp_auth.parse_auth_response_url(url)
        db["acs_tkn"] = sp_auth.get_access_token(code, True, False)
        await message.edit("Авторизация успешна.")
        write_db(db)
    except:
        await message.edit(
            "⚠️Произошла какая-то ошибка. Проверьте, что вы все делаете верно."
        )


@Client.on_message(filters.command("unauth", prefix) & filters.me)
async def unauth(client: Client, message: Message):
    write_db({})
    await message.edit("Данные авторизации удалены успешно.")


@Client.on_message(filters.command("now", prefix) & filters.me)
async def now(client: Client, message: Message):
    db = get_db()
    if db.get("spotify_module", "acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
        current_playback = sp.current_playback()
        try:
            device = (
                current_playback["device"]["name"]
                + " "
                + current_playback["device"]["type"].lower()
            )
        except:
            device = "летающей тарелке"
        try:
            volume = str(current_playback["device"]["volume_percent"]) + "%"
        except:
            volume = "-1%"
        try:
            percentage = ceil(
                current_playback["progress_ms"]
                / current_playback["item"]["duration_ms"]
                * 100
            )
            bar = ""
            bar_filled = ceil(percentage / 10)
            bar_empty = 10 - bar_filled
            for i in range(0, bar_filled):
                bar += "█"
            for i in range(0, bar_empty):
                bar += "░"
            bar += str(" " + str(percentage) + "%")
        except:
            bar = "░░░░░░░░░░ 0%"
        try:
            playlist_id = current_playback["context"]["uri"].split(":")[-1]
            playlist = sp.playlist(playlist_id)
            try:
                playlist_name = playlist["name"]
            except:
                playlist_name = "неизвестен"
            try:
                playlist_owner = (
                    playlist["owner"]["display_name"]
                    + " <code>("
                    + playlist["owner"]["id"]
                    + ")</code>"
                )
            except:
                playlist_owner = "неизвестен"
        except:
            playlist_id = " - "
            playlist_name = " - "
            playlist_owner = " - "
        try:
            track = current_playback["item"]["name"]
            track_id = current_playback["item"]["id"]
        except:
            track = "Не удалось получить трек"
            track_id = "null"
        try:
            track_url = current_playback["item"]["external_urls"]["spotify"]
        except:
            track_url = "undefined"
        artists = []
        try:
            for artist in current_playback["item"]["artists"]:
                artists.append(artist["name"])
        except:
            artists = ["nothing", "here"]

        await message.edit(
            f"Сейчас играет: <code>{track} - {' '.join(artists)}</code> на"
            f" <code>{device}</code>\nСсылки: <a href='{track_url}'>Spotify</a> | <a"
            f" href='https://song.link/s/{track_id}'>Другие платформы</a>\nГромкость:"
            f" <code>{str(volume)}</code>\nПлайлист:"
            f" <code>{playlist_name}</code>\nИдентификатор плейлиста:"
            f" <code>{playlist_id}</code>\nВладелец плейлиста:"
            f" {playlist_owner}\n\nПрогресс: <code>{bar}</code>",
            disable_web_page_preview=True,
        )


@Client.on_message(filters.command("repeat", prefix) & filters.me)
async def repeat(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.repeat("track")
            await message.edit(
                "🔂Поставлено на репит успешно. Счастливого прослушивания!"
            )
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("derepeat", prefix) & filters.me)
async def derepeat(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.repeat("context")
            await message.edit("🎶Снято с репита успешно.")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("next", prefix) & filters.me)
async def next(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.next_track()
            await message.edit("⏭️Трек переключен успешно.")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("pausetr", prefix) & filters.me)
async def pausetr(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.pause_playback()
            await message.edit("⏸️Поставлено на паузу успешно.")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("unpausetr", prefix) & filters.me)
async def unpausetr(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.start_playback()
            await message.edit("▶️Снято с паузы успешно")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("back", prefix) & filters.me)
async def back(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.previous_track()
            await message.edit("◀️Вернул трек назад успешно.")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("restr", prefix) & filters.me)
async def restr(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            sp.seek_track(0)
            await message.edit("🔁Трек перезапущен.")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")


@Client.on_message(filters.command("liketr", prefix) & filters.me)
async def liketr(client: Client, message: Message):
    db = get_db()
    if db.get("acs_tkn") == None:
        await message.edit("⚠️Необходима авторизация. <code>.auth</code>")
    else:
        try:
            sp = spotipy.Spotify(auth=db.get("acs_tkn")["access_token"])
            cupl = sp.current_playback()
            sp.current_user_saved_tracks_add([cupl["item"]["id"]])
            await message.edit("💚Лайкнуто!")
        except:
            await message.edit("⚠️Что-то пошло не так. убедитесь, что трек играет.")
