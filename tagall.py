import asyncio
from time import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pyrogram.callbacks import CallbackQuery

# Import app yang sudah dikonfigurasi dari file main.py
from main import app  # Pastikan app sudah terinisialisasi di main.py

# Durasi pilihan untuk TagAll
DURATIONS = {
    1: "1 menit",
    3: "3 menit",
    5: "5 menit",
    10: "10 menit",
    15: "15 menit",
    20: "20 menit",
    30: "30 menit",
    60: "60 menit",
    120: "120 menit",
    0: "Tanpa Batas"
}

# Fungsi untuk menandai anggota grup
async def tag_all_members(chat_id, members, delay=1):
    for i, member in enumerate(members):
        try:
            user_mention = f"[{member.first_name}](tg://user?id={member.id}) 👋"
            await app.send_message(chat_id, user_mention)
            # Delay setiap 10 anggota
            if i % 10 == 0:
                await asyncio.sleep(delay)
        except FloodWait as e:
            print(f"FloodWait encountered. Waiting for {e.x} seconds.")
            await asyncio.sleep(e.x)  # Tunggu sesuai dengan waktu yang diberikan oleh Telegram

# Fungsi untuk menampilkan gambar grup atau bot
def get_image():
    return "https://upload.wikimedia.org/wikipedia/commons/6/63/Telegram_logo.png"  # Gambar default jika tidak ada gambar grup

# Fitur perintah utag untuk memulai TagAll
@app.on_message(filters.command("utag") & filters.group)
async def tag_all_command(client: Client, message: Message):
    chat_id = message.chat.id
    members = await app.get_chat_members(chat_id)  # Mengambil semua anggota grup
    member_list = [member.user for member in members]  # Mengambil pengguna dari anggota grup

    # Meminta pengguna untuk memilih durasi
    duration_buttons = [
        [InlineKeyboardButton(text=label, callback_data=f"duration_{time}") for time, label in DURATIONS.items()]
    ]
    await message.reply(
        "Pilih durasi TagAll:",
        reply_markup=InlineKeyboardMarkup(duration_buttons),
    )

# Callback untuk memilih durasi
@app.on_callback_query(filters.regex(r"^duration_"))
async def on_duration_selected(client: Client, callback_query: CallbackQuery):
    duration = int(callback_query.data.split("_")[1])

    # Menyediakan durasi dalam pesan
    if duration == 0:  # Tanpa batas waktu
        await callback_query.message.reply("TagAll akan berjalan tanpa batas waktu!")
    else:
        await callback_query.message.reply(f"TagAll akan berjalan selama {DURATIONS[duration]}")

    # Memulai Tagging
    await tag_all_members(callback_query.message.chat.id, member_list, delay=3)

    # Pesan selesai dan jumlah anggota yang telah ditandai
    await callback_query.message.reply(f"TagAll selesai! Total {len(member_list)} anggota telah ditandai.")

    # Tombol Stop TagAll
    stop_button = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="🛑 Stop TagAll", callback_data="stop_tagall")]
    ])
    await callback_query.message.reply("Operasi selesai. Klik untuk menghentikan tagging lebih lanjut.", reply_markup=stop_button)

# Callback untuk menghentikan TagAll
@app.on_callback_query(filters.regex("stop_tagall"))
async def stop_tag_all(client: Client, callback_query: CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer("TagAll dihentikan!", show_alert=True)

# Fungsi tambahan untuk menampilkan jumlah anggota yang ter-tag dalam TagAll
@app.on_callback_query(filters.regex(r"^get_count"))
async def get_tagged_count(client: Client, callback_query: CallbackQuery):
    # Menghitung jumlah anggota yang ter-tag
    total_count = len(await app.get_chat_members(callback_query.message.chat.id))
    await callback_query.answer(f"Jumlah anggota ter-tag: {total_count} anggota.", show_alert=True)

# Link support grup dan emoji
@app.on_message(filters.command("support") & filters.group)
async def support_group(client: Client, message: Message):
    support_message = """
    🌟 **Support Group:** 🌟
    💬 Untuk dukungan lebih lanjut, kunjungi [Support Group](https://t.me/storegarf) kami.
    🎉 Jangan lupa untuk bergabung dan berdiskusi!
    """
    await message.reply(support_message)
