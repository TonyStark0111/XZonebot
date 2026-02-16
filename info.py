import re
from os import environ

# -------------------------
# Helper
# -------------------------
def str_to_bool(val, default=False):
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")

# =========================================================
# 🤖 BOT BASIC INFORMATION
# =========================================================
API_ID = int(environ.get("API_ID", "15529802"))
API_HASH = environ.get("API_HASH", "92bcb6aa798a6f1feadbc917fccb54d3")
BOT_TOKEN = environ.get("BOT_TOKEN", "")
PORT = int(environ.get("PORT", "8080"))
TIMEZONE = environ.get("TIMEZONE", "Asia/Kolkata")
OWNER_USERNAME = environ.get("OWNER_USERNAME", "mrxeontg")

# =========================================================
# 💾 DATABASE CONFIGURATION
# =========================================================
DB_URL = environ.get("DATABASE_URI", "mongodb+srv://XZonebot1:XZonebot1@cluster0.wlxgww7.mongodb.net/?appName=Cluster0")
DB_NAME = environ.get("DATABASE_NAME", "testing")

# =========================================================
# 📢 CHANNELS & ADMINS
# =========================================================
ADMINS = int(environ.get("ADMINS", "821215952"))

LOG_CHANNEL = int(environ.get("LOG_CHANNEL", "-1003747465902"))
PREMIUM_LOGS = int(environ.get("PREMIUM_LOGS", "-1003884967748"))
VERIFIED_LOG = int(environ.get("VERIFIED_LOG", "-1003859075708"))

POST_CHANNEL = int(environ.get("POST_CHANNEL", "-1003801815359"))
VIDEO_CHANNEL = int(environ.get("VIDEO_CHANNEL", "-1003821407875"))
BRAZZER_CHANNEL = int(environ.get("BRAZZER_CHANNEL", "-1003728076805"))

# Auth channels list
auth_channel_str = environ.get("AUTH_CHANNEL", "")
AUTH_CHANNEL = [int(x) for x in auth_channel_str.split() if x.strip().lstrip("-").isdigit()]

# =========================================================
# ⚙️ FEATURES & TOGGLES  (FIXED)
# =========================================================
FSUB = str_to_bool(environ.get("FSUB"), False)
IS_VERIFY = str_to_bool(environ.get("IS_VERIFY"), False)
POST_SHORTLINK = str_to_bool(environ.get("POST_SHORTLINK"), False)
SEND_POST = str_to_bool(environ.get("SEND_POST"), False)
PROTECT_CONTENT = str_to_bool(environ.get("PROTECT_CONTENT"), True)

# =========================================================
# 🔢 LIMITS
# =========================================================
DAILY_LIMIT = int(environ.get("DAILY_LIMIT", "10"))
VERIFICATION_DAILY_LIMIT = int(environ.get("VERIFICATION_DAILY_LIMIT", "20"))
PREMIUM_DAILY_LIMIT = int(environ.get("PREMIUM_DAILY_LIMIT", "50"))
TEMP_PREMIUM_DURATION = int(environ.get("TEMP_PREMIUM_DURATION", "86400"))  # seconds (default 24h)

# =========================================================
# 🔗 SHORTLINK & VERIFICATION
# =========================================================
SHORTLINK_URL = environ.get("SHORTLINK_URL", "")
SHORTLINK_API = environ.get("SHORTLINK_API", "")
POST_SHORTLINK_URL = environ.get("POST_SHORTLINK_URL", "")
POST_SHORTLINK_API = environ.get("POST_SHORTLINK_API", "")
VERIFY_EXPIRE = int(environ.get("VERIFY_EXPIRE", "3600"))
TUTORIAL_LINK = environ.get("TUTORIAL_LINK", "")

# =========================================================
# 💳 PAYMENT SETTINGS
# =========================================================
UPI_ID = environ.get("UPI_ID", "contactxdfc")
QR_CODE_IMAGE = environ.get("QR_CODE_IMAGE", "https://files.catbox.moe/ra46lu.jpg")

# =========================================================
# 🖼️ IMAGES
# =========================================================
START_PIC = environ.get("START_PIC", "https://files.catbox.moe/ra46lu.jpg")
AUTH_PICS = environ.get("AUTH_PICS", "https://files.catbox.moe/ra46lu.jpg")
VERIFY_IMG = environ.get("VERIFY_IMG", "https://files.catbox.moe/ra46lu.jpg")
NO_IMG = environ.get("NO_IMG", "")

# =========================================================
# 🌐 WEB APP
# =========================================================
WEB_APP_URL = environ.get("WEB_APP_URL", "")
