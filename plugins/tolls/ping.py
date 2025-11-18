from datetime import datetime

from pyrogram import filters
from pyrogram.types import Message

from AnonXMusic import app
from AnonXMusic.core.call import Anony
from AnonXMusic.utils import bot_sys_stats
from AnonXMusic.utils.decorators.language import language
from AnonXMusic.utils.inline import supp_markup
from config import BANNED_USERS, PING_IMG_URL


@app.on_message(filters.command(["ping", "alive"]) & ~BANNED_USERS)
@language
async def ping_com(client, message: Message, _):
    # Waktu mulai untuk menghitung respon
    start = datetime.now()

    # Mengirim gambar dan caption pertama kali
    response = await message.reply_photo(
        photo=PING_IMG_URL,  # Gambar yang akan digunakan saat ping
        caption=_["ping_1"].format(app.mention),  # Menyebutkan bot yang digunakan
    )

    # Menghitung waktu ping bot
    pytgping = await Anony.ping()

    # Mengambil status sistem bot (CPU, RAM, DISK)
    UP, CPU, RAM, DISK = await bot_sys_stats()

    # Menghitung waktu respon
    resp = (datetime.now() - start).microseconds / 1000

    # Mengedit pesan dengan detail ping dan status sistem
    await response.edit_text(
        _["ping_2"].format(resp, app.mention, UP, RAM, CPU, DISK, pytgping),
        reply_markup=supp_markup(_),  # Tombol untuk grup support
    )
