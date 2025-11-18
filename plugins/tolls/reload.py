await CallbackQuery.answer()
    basic[videoid] = False
    buttons = queue_back_markup(_, what)
    med = InputMediaPhoto(
        media="https://telegra.ph//file/6f7d35131f69951c74ee5.jpg",
        caption=_["queue_1"],
    )
    await CallbackQuery.edit_message_media(media=med)
    j = 0
    msg = ""
    for x in got:
        j += 1
        msg += f'✨ Title : {x["title"]}\nDuration : {x["dur"]}\nBy : {x["by"]}\n\n'

    if len(msg) < 700:
        await asyncio.sleep(1)
        return await CallbackQuery.edit_message_text(msg, reply_markup=buttons)
    if "✨" in msg:
        msg = msg.replace("✨", "")
    link = await AnonyBin(msg)
    med = InputMediaPhoto(media=link, caption=_["queue_3"].format(link))
    await CallbackQuery.edit_message_media(media=med, reply_markup=buttons)

@app.on_callback_query(filters.regex("queue_back_timer") & ~BANNED_USERS)
@languageCB
async def queue_back(client, CallbackQuery: CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cplay = callback_data.split(None, 1)[1]
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
    
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    
    got = db.get(chat_id)
    if not got:
        return await CallbackQuery.answer(_["queue_2"], show_alert=True)
    
    await CallbackQuery.answer(_["set_cb_5"], show_alert=True)
    file = got[0]["file"]
    videoid = got[0]["vidid"]
    user = got[0]["by"]
    title = (got[0]["title"]).title()
    typo = (got[0]["streamtype"]).title()
    DUR = get_duration(got)
    
    IMAGE = get_image(videoid)  # Gambar yang digunakan dalam antrean

    send = _["queue_6"] if DUR == "Unknown" else _["queue_7"]
    cap = _["queue_8"].format(app.mention, title, typo, user, send)
    upl = (
        queue_markup(_, DUR, cplay, videoid)
        if DUR == "Unknown"
        else queue_markup(_, DUR, cplay, videoid)
    )
    basic[videoid] = True

    med = InputMediaPhoto(media=IMAGE, caption=cap)
    mystic = await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    
    if DUR != "Unknown":
        try:
            while db[chat_id][0]["vidid"] == videoid:
                await asyncio.sleep(5)
                if await is_active_chat(chat_id):
                    if basic[videoid]:
                        pass
                    else:
                        break
                else:
                    break
        except:
            return
