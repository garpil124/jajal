from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import BANNED_USERS, OWNER_ID, SUPPORT_CHAT, PRODUCT_URL

# Mengimpor library yang dibutuhkan untuk pengaturan tambahan
from MyBot import app
from MyBot.utils.database import (
    add_served_chat,
    add_served_user,
    is_banned_user,
    get_lang,
    get_string
)
from MyBot.utils.inline.start import private_panel
from MyBot.utils.inline.settings import setting_markup
from MyBot.utils.decorators.language import LanguageStart, languageCB

# Start Command untuk Private
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    
    # Jika command dengan argumen lebih dari satu
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        
        if name == "help":
            keyboard = private_panel(_)
            return await message.reply_photo(
                photo=START_IMG_URL,  # Ganti dengan gambar yang sesuai
                caption="Welcome to the bot! If you need help, check out our support channel.",
                reply_markup=keyboard
            )
        else:
            # Jika tidak ada command yang cocok
            await message.reply("Invalid command. Please use /help to get the list of commands.")
    else:
        # Jika hanya mengetik /start
        keyboard = private_panel(_)
        await message.reply_photo(
            photo=START_IMG_URL,
            caption=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )


# Start Command untuk Group
@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    uptime = int(time.time() - _boot_)
    await message.reply_photo(
        photo=START_IMG_URL,
        caption=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)


# Welcome New User in Group
@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            
            # Jika user dibanned, ban user tersebut
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass

            if member.id == app.id:
                # Jika bot bergabung dengan grup
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(app.mention, SUPPORT_CHAT),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)
                
                # Menampilkan panel dengan informasi grup
                out = start_panel(_)
                await message.reply_photo(
                    photo=START_IMG_URL,
                    caption=_["start_3"].format(message.from_user.first_name, app.mention),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
