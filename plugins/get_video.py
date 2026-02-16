from os import environ
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from database.users_db import db
from info import PROTECT_CONTENT, DAILY_LIMIT, PREMIUM_DAILY_LIMIT, VERIFICATION_DAILY_LIMIT, FSUB, IS_VERIFY, TEMP_PREMIUM_DURATION
import asyncio
from datetime import datetime, timedelta, timezone
from plugins.verification import av_x_verification
from plugins.ban_manager import ban_manager
from utils import temp, auto_delete_message, is_user_joined

# Import login_start for callback
from plugins.session_login import login_start

@Client.on_message(filters.command("getvideo") | filters.regex(r"(?i)get video"))
async def handle_video_request(client, m: Message):

    # Safety check
    if not m.from_user:
        return

    # Force subscribe check
    if FSUB and not await is_user_joined(client, m):
        return

    user_id = m.from_user.id
    username = m.from_user.username or m.from_user.first_name or "Unknown"

    # Ban check
    if await ban_manager.check_ban(client, m):
        return

    # Premium + limit info
    is_premium = await db.has_premium_access(user_id)
    has_session = await db.get_session(user_id) is not None

    # Define limits based on status
    if is_premium:
        limit = PREMIUM_DAILY_LIMIT
    else:
        limit = DAILY_LIMIT

    used = await db.get_video_count(user_id) or 0

    # ------------------------------------------------
    # LIMIT & VERIFICATION & TEMP PREMIUM SYSTEM
    # ------------------------------------------------

    # Message for when any absolute max limit is reached
    limit_reached_msg = (
        f"𝖸𝗈𝗎'𝗏𝖾 𝖱𝖾𝖺𝖼𝗁𝖾𝖽 𝖸𝗈𝗎𝗋 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍 𝖮𝖿 {used} 𝖥𝗂𝗅𝖾𝗌.\n\n"
        "𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖳𝗈𝗆𝗈𝗋𝗋𝗈𝗐!\n"
        "𝖮𝗋 𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 𝖳𝗈 𝖡𝗈𝗈𝗌𝗍 𝖸𝗈𝗎𝗋 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍"
    )
    buy_button = InlineKeyboardMarkup([
        [InlineKeyboardButton("• 𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇 •", callback_data="get")]
    ])

    if used >= limit:
        # Already premium? Just inform
        if is_premium:
            return await m.reply(
                f"𝖸𝗈𝗎'𝗏𝖾 𝖱𝖾𝖺𝖼𝗁𝖾𝖽 𝖸𝗈𝗎𝗋 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖫𝗂𝗆𝗂𝗍 𝖮𝖿 {PREMIUM_DAILY_LIMIT} 𝖥𝗂𝗅𝖾𝗌.\n"
                f"𝖳𝗋𝗒 𝖠𝗀𝖺𝗂𝗇 𝖳𝗈𝗆𝗈𝗋𝗋𝗈𝗐!"
            )

        # Not premium, check if they have a session
        if has_session:
            # They have a session but no premium: maybe they haven't used temporary bonus yet
            if not await db.has_temp_premium_granted(user_id):
                # Grant temporary premium now
                now = datetime.now(timezone.utc)
                expiry = now + timedelta(seconds=TEMP_PREMIUM_DURATION)
                await db.users.update_one(
                    {"id": user_id},
                    {"$set": {
                        "expiry_time": expiry,
                        "temp_premium_granted": True
                    }}
                )
                # Proceed to send video (they now have premium)
                # No return, continue with video sending
            else:
                # Already used temporary bonus, need to purchase
                return await m.reply(
                    "𝖸𝗈𝗎'𝗏𝖾 𝖠𝗅𝗋𝖾𝖺𝖽𝗒 𝖴𝗌𝖾𝖽 𝖸𝗈𝗎𝗋 𝖳𝖾𝗆𝗉𝗈𝗋𝖺𝗋𝗒 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖡𝗈𝗇𝗎𝗌.\n"
                    "𝖳𝗈 𝖦𝖾𝗍 𝖬𝗈𝗋𝖾 𝖥𝗂𝗅𝖾𝗌, 𝖯𝗅𝖾𝖺𝗌𝖾 𝖯𝗎𝗋𝖼𝗁𝖺𝗌𝖾 𝖺 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇.",
                    reply_markup=buy_button
                )
        else:
            # No session: prompt to login
            login_button = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔐 Login to get Temporary Premium", callback_data="login_prompt")]
            ])
            hours = TEMP_PREMIUM_DURATION // 3600
            return await m.reply(
                f"𝖸𝗈𝗎'𝗏𝖾 𝖱𝖾𝖺𝖼𝗁𝖾𝖽 𝖸𝗈𝗎𝗋 𝖣𝖺𝗂𝗅𝗒 𝖫𝗂𝗆𝗂𝗍 𝖮𝖿 {DAILY_LIMIT} 𝖥𝗂𝗅𝖾𝗌.\n\n"
                f"🔐 **Login with your Telegram account to get {hours} hour{'s' if hours != 1 else ''} of temporary premium access!**",
                reply_markup=login_button
            )

    # ------------------------------------------------
    # GET VIDEO
    # ------------------------------------------------
    video_id = await db.get_unseen_video(user_id)

    if not video_id:
        try:
            video_id = await db.get_random_video()
        except Exception as e:
            print(f"[Random Video Error] {e}")
            return

    if not video_id:
        return await m.reply("❌ No videos found in the database.")

    # ------------------------------------------------
    # SEND VIDEO
    # ------------------------------------------------
    try:
        sent = await client.send_video(
            chat_id=m.chat.id,
            video=video_id,
            protect_content=PROTECT_CONTENT,
            caption=(
                f"𝘗𝘰𝘸𝘦𝘳𝘦𝘥 𝘉𝘺: {temp.B_LINK}\n\n"
                "<blockquote>"
                "ᴛʜɪꜱ ꜰɪʟᴇ ᴡɪʟʟ ʙᴇ ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀꜰᴛᴇʀ 10 ᴍɪɴᴜᴛᴇꜱ.\n"
                "ᴘʟᴇᴀꜱᴇ ꜰᴏʀᴡᴀʀᴅ ᴛʜɪꜱ ꜰɪʟᴇ ꜱᴏᴍᴇᴡʜᴇʀᴇ ᴇʟꜱᴇ "
                "ᴏʀ ꜱᴀᴠᴇ ɪɴ ꜱᴀᴠᴇᴅ ᴍᴇꜱꜱᴀɢᴇꜱ."
                "</blockquote>"
            ),
            reply_to_message_id=m.id
        )

        # Increase daily count ONLY after successful send
        await db.increase_video_count(user_id, username)

        # Auto delete in background
        asyncio.create_task(auto_delete_message(m, sent))

    except Exception as e:
        await m.reply(f"❌ Failed to send video: {str(e)}")
