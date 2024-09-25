import asyncio
from config import Config
from pyrogram import Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.enums import ParseMode

async def ForceSub(bot: Client, update: Message):
    """
    Custom Pyrogram Based Telegram Bot's Force Subscribe Function by @ZauteKm.
    If User is not Joined Force Sub Channel Bot to Send a Message & ask him to Join First.
    
    :param bot: Pass Client.
    :param event: Pass Message.
    :return: It will return 200 if Successfully Got User in Force Sub Channel and 400 if Found that User Not Participant in Force Sub Channel or User is Kicked from Force Sub Channel it will return 400. Also it returns 200 if Unable to Find Channel.
    """
    
    try:
        invite_link = await bot.create_chat_invite_link(chat_id=(int(Config.AUTH_CHANNEL) if Config.AUTH_CHANNEL.startswith("-100") else Config.AUTH_CHANNEL))
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update)
        return fix_
    except Exception as err:
        print(f"Unable to do Force Subscribe to {Config.AUTH_CHANNEL}\n\nError: {err}\n\nContact Support Group: https://t.me/JOSPSupport")
        return 200
    try:
        user = await bot.get_chat_member(chat_id=(int(Config.AUTH_CHANNEL) if Config.AUTH_CHANNEL.startswith("-100") else Config.AUTH_CHANNEL), user_id=update.from_user.id)
        if user.status == "kicked":
            await bot.send_message(
                chat_id=update.from_user.id,
                text="Sorry Sir, You are Banned to use me. Contact my [Support Group](https://t.me/JOSPSupport).",
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_to_message_id=update.id
            )
            return 400
        else:
            return 200
    except UserNotParticipant:
        await bot.send_message(
            chat_id=update.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**\n\nDue to Overload, Only Channel Subscribers can use the Bot!",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            ),
            parse_mode=ParseMode.MARKDOWN,
            reply_to_message_id=update.id
        )
        return 400
    except FloodWait as e:
        await asyncio.sleep(e.x)
        fix_ = await ForceSub(bot, update)
        return fix_
    except Exception as err:
        print(f"Something Went Wrong! Unable to do Force Subscribe.\nError: {err}\n\nContact Support Group: https://t.me/JOSPSupport")
        return 200
