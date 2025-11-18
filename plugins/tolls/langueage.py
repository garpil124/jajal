from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, Message
from pykeyboard import InlineKeyboard  # Pastikan menggunakan implementasi InlineKeyboard yang benar

from YourBot import app  # Sesuaikan dengan nama bot kamu
from YourBot.utils.database import get_lang, set_lang  # Pastikan ini mengarah ke utilitas yang sesuai
from YourBot.utils.decorators import ActualAdminCB, language, languageCB  # Sesuaikan dekorator
from config import BANNED_USERS
from strings import get_string, languages_present  # Update dengan file strings kamu


# Fungsi untuk membuat tombol pilihan bahasa
def lanuages_keyboard(_):
    keyboard = InlineKeyboard(row_width=2)
    keyboard.add(
        *[
            InlineKeyboardButton(
                text=languages_present[i],
                callback_data=f"languages:{i}",
            )
            for i in languages_present
        ]
    )
    keyboard.row(
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],  # Pastikan sudah didefinisikan di strings
            callback_data="settingsback_helper",
        ),
        InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close"),
    )
    return keyboard


# Perintah untuk menampilkan pilihan bahasa
@app.on_message(filters.command(["lang", "setlang", "language"]) & ~BANNED_USERS)
@language
async def langs_command(client, message: Message, _):
    keyboard = lanuages_keyboard(_)
    await message.reply_text(
        _["lang_1"],  # Pastikan pesan ini ada di file strings
        reply_markup=keyboard,
    )


# Callback untuk menampilkan pilihan bahasa lagi ketika tombol diklik
@app.on_callback_query(filters.regex("LG") & ~BANNED_USERS)
@languageCB
async def lanuagecb(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)


# Callback untuk menangani pemilihan bahasa
@app.on_callback_query(filters.regex(r"languages:(.*?)") & ~BANNED_USERS)
@ActualAdminCB
async def language_markup(client, CallbackQuery, _):
    langauge = (CallbackQuery.data).split(":")[1]
    old = await get_lang(CallbackQuery.message.chat.id)
    if str(old) == str(langauge):
        return await CallbackQuery.answer(_["lang_4"], show_alert=True)  # Sudah menggunakan bahasa yang sama
    try:
        _ = get_string(langauge)
        await CallbackQuery.answer(_["lang_2"], show_alert=True)  # Bahasa berhasil diubah
    except:
        _ = get_string(old)
        return await CallbackQuery.answer(
            _["lang_3"],  # Jika bahasa tidak ditemukan
            show_alert=True,
        )
    await set_lang(CallbackQuery.message.chat.id, langauge)
    keyboard = lanuages_keyboard(_)
    return await CallbackQuery.edit_message_reply_markup(reply_markup=keyboard)
