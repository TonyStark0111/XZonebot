# plugins/session_login.py

import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors import (
    PhoneNumberInvalid,
    PhoneCodeInvalid,
    PhoneCodeExpired,
    SessionPasswordNeeded,
    PasswordHashInvalid,
    FloodWait
)
from datetime import datetime, timedelta, timezone
from info import API_ID, API_HASH, TEMP_PREMIUM_DURATION
from database.users_db import db

# Store login states: {user_id: {'step': str, 'client': Client, 'phone': str, 'hash': str}}
LOGIN_STATES = {}

# Step names
STEP_PHONE = "phone"
STEP_CODE = "code"
STEP_PASSWORD = "password"

# ================ COMMANDS ================

@Client.on_message(filters.private & filters.command("login"))
async def login_start(client: Client, message: Message):
    user_id = message.from_user.id

    # Already logged in?
    if await db.get_session(user_id):
        return await message.reply(
            "✅ You're already logged in!\n\nUse /logout to switch accounts.",
            parse_mode=enums.ParseMode.HTML
        )

    # If already in login process, cancel it first
    if user_id in LOGIN_STATES:
        old_state = LOGIN_STATES[user_id]
        if 'client' in old_state:
            try:
                await old_state['client'].disconnect()
            except:
                pass
        del LOGIN_STATES[user_id]

    # Start new login
    msg = await message.reply(
        "📞 **Please send your phone number** with country code.\n"
        "Example: `+919876543210`\n\n"
        "You can cancel at any time by pressing the button below.",
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("❌ Cancel", callback_data="login_cancel")
        ]])
    )
    # Store state
    LOGIN_STATES[user_id] = {
        'step': STEP_PHONE,
        'message_id': msg.id,
        'client': None
    }

@Client.on_message(filters.private & filters.command("logout"))
async def logout_command(client: Client, message: Message):
    user_id = message.from_user.id
    # Clear any active login
    if user_id in LOGIN_STATES:
        state = LOGIN_STATES[user_id]
        if 'client' in state:
            try:
                await state['client'].disconnect()
            except:
                pass
        del LOGIN_STATES[user_id]
    # Remove session from DB
    await db.delete_session(user_id)
    await message.reply("✅ Logged out successfully.", parse_mode=enums.ParseMode.HTML)

@Client.on_message(filters.private & filters.command("cancel"))
async def cancel_command(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id in LOGIN_STATES:
        state = LOGIN_STATES[user_id]
        if 'client' in state:
            try:
                await state['client'].disconnect()
            except:
                pass
        del LOGIN_STATES[user_id]
        await message.reply("❌ Login cancelled.", parse_mode=enums.ParseMode.HTML)
    else:
        await message.reply("No active login to cancel.")

# ================ CALLBACKS ================

@Client.on_callback_query(filters.regex("^login_cancel$"))
async def login_cancel_callback(client: Client, callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in LOGIN_STATES:
        state = LOGIN_STATES[user_id]
        if 'client' in state:
            try:
                await state['client'].disconnect()
            except:
                pass
        del LOGIN_STATES[user_id]
    await callback.message.delete()
    await callback.answer("Login cancelled.", show_alert=True)

# ================ TEXT HANDLER ================

@Client.on_message(filters.private & filters.text & ~filters.command(["start", "login", "logout", "cancel"]))
async def login_text_handler(client: Client, message: Message):
    user_id = message.from_user.id
    if user_id not in LOGIN_STATES:
        return

    state = LOGIN_STATES[user_id]
    step = state['step']
    text = message.text.strip()

    # Cancel if user types "cancel" (case-insensitive)
    if text.lower() == "cancel":
        if 'client' in state:
            try:
                await state['client'].disconnect()
            except:
                pass
        del LOGIN_STATES[user_id]
        await message.reply("❌ Login cancelled.", reply_markup=None)
        return

    # Step: Phone number
    if step == STEP_PHONE:
        phone = text.replace(" ", "")
        if not phone.startswith("+"):
            phone = "+" + phone

        # Create temporary client
        temp_client = Client(
            name=f"session_{user_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True
        )

        status_msg = await message.reply("🔄 Connecting to Telegram...")

        try:
            await temp_client.connect()
            sent_code = await temp_client.send_code(phone)

            # Update state
            state['step'] = STEP_CODE
            state['client'] = temp_client
            state['phone'] = phone
            state['hash'] = sent_code.phone_code_hash

            await status_msg.edit(
                "📲 **Verification code sent!**\n\n"
                "Please enter the code you received in your Telegram app.\n"
                "You can send it with or without spaces.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("❌ Cancel", callback_data="login_cancel")
                ]])
            )
        except PhoneNumberInvalid:
            await status_msg.edit("❌ Invalid phone number. Please try again with /login.")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        except Exception as e:
            await status_msg.edit(f"❌ Error: {str(e)}")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        finally:
            await message.delete()

    # Step: Verification code
    elif step == STEP_CODE:
        code = text.replace(" ", "")
        temp_client = state['client']
        phone = state['phone']
        phone_hash = state['hash']

        status_msg = await message.reply("🔄 Verifying code...")

        try:
            await temp_client.sign_in(phone, phone_hash, code)
            # If no 2FA, login successful
            await finalize_login(status_msg, temp_client, user_id)
        except SessionPasswordNeeded:
            state['step'] = STEP_PASSWORD
            await status_msg.edit(
                "🔐 **Two‑step verification enabled.**\n\nPlease enter your password.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("❌ Cancel", callback_data="login_cancel")
                ]])
            )
        except PhoneCodeInvalid:
            await status_msg.edit("❌ Invalid code. Please try again with /login.")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        except PhoneCodeExpired:
            await status_msg.edit("❌ Code expired. Please restart with /login.")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        except Exception as e:
            await status_msg.edit(f"❌ Error: {str(e)}")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        finally:
            await message.delete()

    # Step: Password (2FA)
    elif step == STEP_PASSWORD:
        password = text
        temp_client = state['client']

        status_msg = await message.reply("🔄 Verifying password...")

        try:
            await temp_client.check_password(password)
            await finalize_login(status_msg, temp_client, user_id)
        except PasswordHashInvalid:
            await status_msg.edit("❌ Incorrect password. Please try again with /login.")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        except Exception as e:
            await status_msg.edit(f"❌ Error: {str(e)}")
            await temp_client.disconnect()
            del LOGIN_STATES[user_id]
        finally:
            await message.delete()

# ================ FINALIZE LOGIN ================

async def finalize_login(status_msg: Message, temp_client: Client, user_id: int):
    try:
        # Export session string
        session_string = await temp_client.export_session_string()
        await temp_client.disconnect()

        # Save session in DB
        await db.set_session(user_id, session_string)

        # Grant temporary premium if not already granted
        if not await db.has_temp_premium_granted(user_id):
            now = datetime.now(timezone.utc)
            expiry = now + timedelta(seconds=TEMP_PREMIUM_DURATION)
            await db.users.update_one(
                {"id": user_id},
                {"$set": {
                    "expiry_time": expiry,
                    "temp_premium_granted": True
                }}
            )
            hours = TEMP_PREMIUM_DURATION // 3600
            bonus_msg = f"\n\n🎁 You've been granted **{hours} hour{'s' if hours != 1 else ''}** of temporary premium access!"
        else:
            bonus_msg = ""

        # Clear state
        if user_id in LOGIN_STATES:
            del LOGIN_STATES[user_id]

        await status_msg.edit(
            f"✅ **Login successful!**{bonus_msg}\n\n"
            "Your session has been saved securely. You can now enjoy higher limits.",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        await status_msg.edit(f"❌ Failed to save session: {str(e)}")
        if user_id in LOGIN_STATES:
            del LOGIN_STATES[user_id]
