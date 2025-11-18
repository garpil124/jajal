import asyncio
import importlib
import time

from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall

import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from AnonXMusic.plugins.tools.tagall import client
from AnonXMusic.utils.inline import supp_markup

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(name).error("Assistant client variables not defined, exiting...")
        exit()
    await sudo()
    
    # Adding banned users to BANNED_USERS
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass

    # Start the main bot
    await app.start()
    
    # Import all modules
    for all_module in ALL_MODULES:
        importlib.import_module("AnonXMusic.plugins" + all_module)
    LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")
    
    # Start userbot and video call (no music, no YouTube)
    await userbot.start()
    await Anony.start()
    
    # Handle TagAll with duration
    LOGGER("AnonXMusic").info("Adding custom support for TagAll and user interaction...")
    await Anony.decorators()

    # Start video call if needed (without music/video)
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error(
            "Please turn on the videochat of your log group/channel.\n\nStopping Bot..."
        )
        exit()
    except:
        pass
    
    # Display success message
    LOGGER("AnonXMusic").info(
        "Bot started successfully.\n\nYou can now interact with your bot and use commands!"
    )
    
    # Handling interaction with the bot
    await idle()
    
    # Shutdown gracefully
    await app.stop()
    await userbot.stop()
    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
