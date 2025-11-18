from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle
from config import BANNED_USERS

from MyBot import app
from MyBot.utils.database import get_lang
from MyBot.utils.inline import product_markup, support_markup
from strings import get_string


@app.on_inline_query(~BANNED_USERS)
async def inline_query_handler(client, query):
    text = query.query.strip().lower()
    answers = []
    
    # Jika query kosong, tampilkan menu umum
    if text.strip() == "":
        # Menampilkan menu produk atau informasi umum
        product_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("💥 Produk Kami", callback_data="products")]]
        )
        support_button = InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎮 Grup Support", url="https://t.me/YourSupportGroup")]]
        )

        answers.append(
            InlineQueryResultArticle(
                title="Selamat datang di Bot!",
                input_message_content="Hi! Klik tombol di bawah untuk mulai.",
                reply_markup=product_button,
                description="Tombol untuk melihat produk kami",
            )
        )

        answers.append(
            InlineQueryResultArticle(
                title="Grup Support",
                input_message_content="Bergabunglah dengan grup support kami!",
                reply_markup=support_button,
                description="Tombol untuk menuju grup support",
            )
        )

        try:
            await client.answer_inline_query(query.id, results=answers, cache_time=10)
        except Exception as e:
            print(f"Error: {e}")
            return

    else:
        # Pencarian produk atau fitur tertentu (contoh: cari produk)
        if "produk" in text:
            # Ganti dengan logika pencarian produk yang relevan
            answers.append(
                InlineQueryResultArticle(
                    title="Produk A",
                    input_message_content="Ini adalah produk A.",
                    description="Deskripsi produk A",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Beli Sekarang", url="https://t.me/YourProductLink")
                            ]
                        ]
                    ),
                )
            )

            answers.append(
                InlineQueryResultArticle(
                    title="Produk B",
                    input_message_content="Ini adalah produk B.",
                    description="Deskripsi produk B",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("Beli Sekarang", url="https://t.me/YourProductLink")
                            ]
                        ]
                    ),
                )
            )

            try:
                await client.answer_inline_query(query.id, results=answers, cache_time=10)
            except Exception as e:
                print(f"Error: {e}")
                return
