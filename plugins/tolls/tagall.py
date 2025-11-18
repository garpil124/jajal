import os, logging, asyncio, random
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin, ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

from config import BOT_TOKEN as bot_token, API_ID as api_id, API_HASH as api_hash

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("log.txt"),
        logging.StreamHandler(),
    ],
)

client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)

spam_chats = []

# Daftar grup support dan creator bot
SUPPORT_GROUP = 'your_support_group_link_or_chat_id'  # Ganti dengan link support grup
CREATOR_ID = 123456789  # Ganti dengan ID creator

# Durasi TagAll dalam menit
durations = [
    ("1 menit", 1),
    ("5 menit", 5),
    ("10 menit", 10),
    ("15 menit", 15),
    ("20 menit", 20),
    ("30 menit", 30),
    ("45 menit", 45),
    ("60 menit", 60)
]

# Fungsi untuk memeriksa apakah pengguna adalah admin atau pemilik bot
async def is_admin_or_creator(event):
    is_admin = False
    try:
        partici_ = await client(GetParticipantRequest(
            event.chat_id,
            event.sender_id
        ))
    except UserNotParticipantError:
        is_admin = False
    else:
        if (
                isinstance(
                    partici_.participant,
                    (
                            ChannelParticipantAdmin,
                            ChannelParticipantCreator
                    )
                )
        ):
            is_admin = True
    return is_admin

@client.on(events.NewMessage(pattern="^/utag ?(.*)"))
async def mentionall(event):
    chat_id = event.chat_id
    if event.is_private:
        return await event.respond("Perintah ini hanya digunakan dalam grup dan channel.")

    is_admin = await is_admin_or_creator(event)
    if not is_admin:
        return await event.reply("Hanya admin yang dapat menjalankan perintah ini...")

    # Jika ada teks yang disertakan dengan perintah atau pesan yang dibalas
    if event.pattern_match.group(1) and event.is_reply:
        return await event.reply("Berikan beberapa teks atau balas pesan..")
    elif event.pattern_match.group(1):
        mode = "text_on_cmd"
        msg = event.pattern_match.group(1)
    elif event.is_reply:
        mode = "text_on_reply"
        msg = await event.get_reply_message()
        if msg == None:
            return await event.respond(
                "Saya tidak bisa menyebut anggota untuk pesan lama! (pesan yang dikirim sebelum saya ditambahkan ke grup)")
    else:
        return await event.reply("Berikan beberapa teks atau balas pesan..")

    # Menampilkan button durasi
    buttons = [
        [Button.inline(f"{text}", data=f"set_duration_{duration}") for text, duration in durations]
    ]
    await event.reply("Pilih durasi TagAll:", buttons=buttons)

# Menangani pemilihan durasi
@client.on(events.CallbackQuery(pattern=r"set_duration_(\d+)"))
async def set_duration(event: CallbackQuery):
    duration = int(event.data.decode().split("_")[2])
    # Simpan durasi dan lanjutkan dengan pengiriman pesan TagAll
    # Tindak lanjut di sini, misalnya memberi tahu pemilih durasi
    await event.answer(f"Durasi TagAll: {duration} menit")
    await event.respond("TagAll dimulai dengan durasi yang dipilih.")

    # Loading message
    loading_message = await event.respond("⏳ Memulai proses TagAll... tunggu sebentar!")

    # Proses untuk menjalankan TagAll sesuai durasi yang dipilih
    spam_chats.append(chat_id)
    usrnum = 0
    usrtxt = ''
    async for usr in client.iter_participants(chat_id):

if not chat_id in spam_chats:
            break
        usrnum += 1
        usrtxt += f"🐣 [{usr.first_name}](tg://user?id={usr.id})\n"
        if usrnum == 5:
            if mode == "text_on_cmd":
                txt = f"{msg}\n\n{usrtxt}"
                await client.send_message(chat_id, txt)
            elif mode == "text_on_reply":
                await msg.reply(usrtxt)
            await asyncio.sleep(2)
            usrnum = 0
            usrtxt = ''
    try:
        spam_chats.remove(chat_id)
    except:
        pass
    await loading_message.edit("✅ TagAll selesai!")

    # Informasi tambahan
    await event.respond(f"✔️ Total TagAll selesai! {usrnum} anggota ter-tag.")
    await event.respond(f"💬 Untuk support, kunjungi grup: {SUPPORT_GROUP}")
    await event.respond(f"👨‍💻 Bot Creator: [Your Creator Name](tg://user?id={CREATOR_ID})")

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
    is_admin = await is_admin_or_creator(event)
    if not is_admin:
        return await event.reply("Hanya admin yang dapat menjalankan perintah ini...")
    if not event.chat_id in spam_chats:
        return await event.reply("Tidak ada mention!")
    else:
        try:
            spam_chats.remove(event.chat_id)
        except:
            pass
        return await event.respond("Dihentikan!")

client.run_until_disconnected()
