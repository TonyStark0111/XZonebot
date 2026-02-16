# 🤖 Pron Wali Zone Adult Zone

A simple yet powerful Pron Wali Zone Adult Zone Telegram bot to manage premium video subscriptions, daily limits, and auto-delete functionalities. Built with Pyrogram and MongoDB.

---

## 🌟 Features

- **💎 Premium System:** Monthly subscription management with expiry tracking.
- **📸 Screenshot Verification:** Users send payment screenshots, Admins approve/reject via buttons.
- **🔢 Daily Limits:** Different file limits for Free vs Premium users.
- **⏳ Auto-Delete:** Videos are automatically deleted after a set time (10 mins).
- **🚫 Ban Manager:** Built-in system to ban malicious users.
- **🖼️ Auto Poster:** Automatically posts new videos with thumbnails to your channel.
- **🤝 Referral System:** Users can invite friends via unique links to earn rewards.
- **📊 Advanced Stats:** View detailed real-time statistics of total users and database.
- **📂 Advanced Indexing:** Automatically saves/indexes files from multiple source channels.
- **🔐 Verification System:** Secure verification process to filter spammers.
- **🎁 Redeem System:** Support for promo codes to redeem premium access.
- **🔗 Shortlink Support:** Monetize content by enabling shortlinks for free users.
- **📄 User Reports:** Generates daily `.txt` reports of active and premium users for Admins.
- **⏰ Expiry Reminders:** Automatically notifies users when their premium plan is about to expire.
- **📢 Force Subscribe:** Forces users to join a channel before using the bot.

## 🛠 Config Variables

You need to set up the following environment variables in your `.env` file or Cloud Dashboard.

| Variable | Description |
| :--- | :--- |
| `API_ID` | Your Telegram API ID (from my.telegram.org) |
| `API_HASH` | Your Telegram API Hash |
| `BOT_TOKEN` | Your Bot Token (from @BotFather) |
| `DB_URI` | MongoDB Connection String |
| `DB_NAME` | Your Database Name |
| `ADMINS` | Admin ID |
| `LOG_CHANNEL` | Log Channel ID |

---

### 👇 Copy for .env file

```env
API_ID=21958
API_HASH=812529f879f05c7d62eb49f5d1
BOT_TOKEN=7097168:AAF8T3ijc21xIUUuseLU41xa5bRA
DB_URI=mongodb+srv://testing1:axxxz@testing.kwuyv1poka.mongodb.net/?appName=testing
DB_NAME=testing
ADMINS=5977931010
LOG_CHANNEL=-10000000
```

## 🚀 Deployment

Choose your preferred method to deploy the bot.

### 💜 Heroku (Easiest)

<p align="left">
  <a href="https://heroku.com/deploy?template=https://github.com/Botsthe/PronWaliZoneBot">
    <img src="https://www.herokucdn.com/deploy/button.svg" alt="Deploy to Heroku">
  </a>
</p>

1. Click the button above.
2. Enter your App Name.
3. Fill in the **Config Variables** (API_ID, BOT_TOKEN, etc.).
4. Click **Deploy App**.
5. Once deployed, turn on the **Worker Dyno** in the "Resources" tab.

---

### 💙 Koyeb (Fast & Free)

<p align="left">
  <a href="https://app.koyeb.com/deploy?type=git&repository=Botsthe/PronWaliZoneBot&branch=main&name=pronwalizone">
    <img src="https://www.koyeb.com/static/images/deploy/button.svg" alt="Deploy to Koyeb">
  </a>
</p>

1. Click the button above.
2. Sign in with GitHub.
3. In **Environment Variables**, add all your vars (`API_ID`, `BOT_TOKEN`, etc.).
4. Click **Deploy**.

---

### ☁️ Render (Stable)

<p align="left">
  <a href="https://render.com/deploy?repo=https://github.com/Botsthe/PronWaliZoneBot">
    <img src="https://render.com/images/deploy-to-render-button.svg" alt="Deploy to Render">
  </a>
</p>

1. Click the button or go to [Render Dashboard](https://dashboard.render.com/).
2. Select **"Web Service"**.
3. Connect your GitHub repository.
4. **Settings:**
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
5. Go to the **Environment** tab and add all your variables.
6. Click **Create Web Service**.

---

### 💻 VPS / Local System
```Method 1: Docker (Recommended)

# 1. Clone Repository
git clone [https://github.com/Botsthe/PronWaliZoneBot.git](https://github.com/Botsthe/PronWaliZoneBot.git)
cd PronWaliZoneBot

# 2. Install Requirements
pip3 install -U -r requirements.txt

# 3. Create .env file and fill details (or edit info.py)
nano .env

# 4. Run Bot
python3 bot.py
```
---

## 🤖 Bot Commands

### 👤 User Commands

| Command | Description |
| :--- | :--- |
| `/start` | Start the bot and check if it is alive. |
| `/myplan` | Check your current subscription plan and daily limit. |
| `/buy` | Get Premium plan details and payment QR Code. |
| `/brazzers` | Request a random video file (Premium/Limited). |
| `/getvideo` | Request a random video file (Premium/Limited/verification). |
| `/refer` | Get your referral link to invite friends. |
| `/redeem` | Redeem a premium code. |
| `/help` | Get help regarding bot usage. |
| `/about` | Information about the bot and developer. |
| `/terms` | View Terms and Conditions. |
| `/disclaimer` | View Legal Disclaimer. |

---

### 👑 Admin Commands

**ℹ️ Note:** You can use `/owner_cmd` to see all admin commands in the bot itself.

#### 💎 Premium & Redeem Management
- `/add_premium [user_id] [time]` - Give premium (e.g., `/add_premium 12345 1 month`).
- `/remove_premium [user_id]` - Remove premium access from a user.
- `/premium_user` - Get a list (`.txt` file) of all active paid users.
- `/code [time]` - Generate a redeem code (e.g., `/code 1 month`).
- `/allcodes` - List all active redeem codes.
- `/clearcodes` - Delete all active redeem codes.
- `/delete_redeem [code]` - Delete a specific redeem code.

#### 🚫 User Management
- `/ban [user_id]` - Ban a user from using the bot.
- `/unban [user_id]` - Unban a user.
- `/blocked` - Get a list of all banned users.
- `/check_user [user_id]` - Check details of a specific user.
- `/all_users_stats` - Get a daily report of all users.

#### ⚙️ System & Broadcast
- `/stats` - Check database statistics.
- `/broadcast` - Broadcast a message to all users (Reply to a message).
- `/index` - Index files from a channel manually.
- `/deleteall` - Delete all files from the database (Use with caution).
- `/owner_cmd` - Show the Admin Help Menu.

#### 👇 Copy for set command bot father 

``` command
start - 🟢 𝖲𝗍𝖺𝗋𝗍 𝖳𝗁𝖾 𝖡𝗈𝗍
myplan - 📊 𝖢𝗁𝖾𝖼𝗄 𝖬𝗒 𝖯𝗅𝖺𝗇 & 𝖫𝗂𝗆𝗂𝗍
buy - 💎 𝖡𝗎𝗒 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖲𝗎𝖻𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇
getvideo - 🎬 𝖦𝖾𝗍 𝖵𝗂𝖽𝖾𝗈 (𝖵𝖾𝗋𝗂𝖿𝗒/𝖯𝗋𝖾𝗆)
brazzers - 🔥 𝖦𝖾𝗍 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖵𝗂𝖽𝖾𝗈
refer - 🤝 𝖨𝗇𝗏𝗂𝗍𝖾 & 𝖤𝖺𝗋𝗇
redeem - 🎁 𝖱𝖾𝖽𝖾𝖾𝗆 𝖯𝗋𝖾𝗆𝗂𝗎𝗆 𝖢𝗈𝖽𝖾
help - ℹ️ 𝖧𝖾𝗅𝗉 & 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌
about - 👨‍💻 𝖠𝖻𝗈𝗎𝗍 𝖣𝖾𝗏𝖾𝗅𝗈𝗉𝖾𝗋
terms - 📜 𝖳𝖾𝗋𝗆𝗌 & 𝖢𝗈𝗇𝖽𝗂𝗍𝗂𝗈𝗇𝗌
disclaimer - ⚠️ 𝖫𝖾𝗀𝖺𝗅 𝖣𝗂𝗌𝖼𝗅𝖺𝗂𝗆𝖾𝗋
owner_cmd - 👑 𝖠𝖽𝗆𝗂𝗇 𝖢𝗈𝗆𝗆𝖺𝗇𝖽𝗌 𝖬𝖾𝗇𝗎
```


---


<p align="center">
  <a href="https://t.me/PronWaliZoneBot">
    <img src="https://img.shields.io/badge/🤖%20START%20DEMO%20BOT-blue?style=for-the-badge&logo=telegram">
  </a>
  <a href="https://t.me/AV_SUPPORT_GROUP">
    <img src="https://img.shields.io/badge/💬%20JOIN%20SUPPORT-black?style=for-the-badge&logo=telegram">
  </a>
</p>

---

<h2 align="center">👨‍💻 DEVELOPER & CREDITS</h2>

<p align="center">
  <b>👑 OWNER & DEVELOPER: <a href="https://t.me/BOT_OWNER26">AMAN VISHWAKARMA</a></b>
</p>

<p align="center">
  <a href="https://github.com/Botsthe">
    <img src="https://img.shields.io/github/followers/Botsthe?style=social&label=Follow&style=flat-square">
  </a>
  <a href="https://t.me/BOT_OWNER26">
    <img src="https://img.shields.io/badge/Telegram-DM%20Me-blue?style=flat-square&logo=telegram">
  </a>
  <a href="https://av-botz.vercel.app/">
    <img src="https://img.shields.io/badge/Official-Website-black?style=flat-square&logo=google-chrome">
  </a>
</p>

---

<h2 align="center">💖 SUPPORT & DONATION</h2>

<p align="center">
  If you like this project, please consider donating to keep the servers alive!
</p>

<p align="center">
  <a href="https://av-botz.vercel.app/pay">
    <img src="https://img.shields.io/badge/☕%20DONATE%20VIA%20UPI%20%2F%20QR-CLICK%20HERE-green?style=for-the-badge">
  </a>
</p>
<p align="center">
  <a href="https://av-botz.vercel.app/pay">
    <img src="https://img.shields.io/badge/🥤%20BUY%20ME%20A%20COFFEE-yellow?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black">
  </a>
</p>

<p align="center">
  <i>Every donation helps in maintaining the bot and adding new features!</i>
</p>

---

<h2 align="center">📌 IMPORTANT NOTE</h2>

<p align="center">
  <b>Copying or Selling this repo is strictly prohibited.</b>
</p>

<p align="center">
  <i>This project is protected by Copyright © 2026 AV BOTZ. Any violation will be reported immediately.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/⛔%20No%20Reselling-red?style=flat-square">
  <img src="https://img.shields.io/badge/✅%20Open%20Source-green?style=flat-square">
</p>

---

<h3 align="center">
  Powered by <a href="https://av-botz.vercel.app/">AV BOTZ</a> © 2025
</h3>

