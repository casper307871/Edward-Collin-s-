#!/usr/bin/env python3
"""Edward Admin Bot v2 – with help menu, structured commands, and cleaner formatting."""

import json, os, logging
from functools import wraps
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# 🔒 Hard-coded BOT TOKEN
BOT_TOKEN = "bot token "

# 🔒 Permanent founders (cannot ever be removed)
PERMANENT_FOUNDERS = {6328533463}

# 💾 Persistent data file
DATA_FILE = "data.json"

# 🧠 Logging setup
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("EdwardBot")


# ─────────────────────────────────────────────────────────────
# Database Helpers
# ─────────────────────────────────────────────────────────────
def load_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(
                {
                    "founders_dynamic": [],
                    "gbans": [],
                    "fbans": [],
                    "enforced_groups": [],
                    "federation_groups": [],
                    "secure_mode": True,
                    "shadowbans": [],
                },
                f,
                indent=2,
            )
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_db(db):
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=2)


# ─────────────────────────────────────────────────────────────
# Access Control
# ─────────────────────────────────────────────────────────────
def is_founder(user_id: int) -> bool:
    db = load_db()
    dynamic = set(db.get("founders_dynamic", []))
    return user_id in PERMANENT_FOUNDERS or user_id in dynamic


def founders_list():
    db = load_db()
    dynamic = db.get("founders_dynamic", [])
    return sorted(list(PERMANENT_FOUNDERS) + dynamic)


def founder_required(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        user = update.effective_user
        if not user or not is_founder(user.id):
            if update.message:
                await update.message.reply_text("⛔ You must be a founder to use this command.")
            return
        return await func(update, context, *args, **kwargs)

    return wrapped


# ─────────────────────────────────────────────────────────────
# Commands
# ─────────────────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Edward Admin Bot is active.\nUse /help for available commands.")


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🤖 **Edward Admin Bot Commands:**\n\n"
        "📘 **General Commands:**\n"
        "• /start – Check if the bot is running.\n"
        "• /help – Show this help message.\n"
        "• /settings – Display key configuration values.\n"
        "• /logs – Show recent bot log entries.\n"
        "• /getgroupinfo – Show info about the current group.\n\n"
        "👑 **Founder Tools:**\n"
        "• /panel, /status, /fed – Show system statistics.\n"
        "• /addfounder <user_id>, /removefounder <user_id>, /founders – Manage founders.\n"
        "• /secure on|off – Toggle secure mode.\n"
        "• /gban <user_id> [reason], /ungban <user_id> – Manage global bans.\n"
        "• /fban <user_id> [reason], /unfban <user_id> – Manage federation bans.\n"
        "• /banlist – Show global and federation ban lists.\n"
        "• /enforce <group_id>, /unenforce <group_id> – Manage enforced groups.\n"
        "• /fedadd <group_id>, /fedremove <group_id>, /fedgroups – Manage federation groups.\n"
        "• /listgroups – List all enforced groups.\n"
        "• /shadowban <user_id>, /unshadowban <user_id> – Manage shadowbans.\n"
        "• /shadowmode [on|off] – Toggle shadowban enforcement.\n"
        "• /whois <user_id> – Look up a user’s info.\n"
        "• /history <user_id> – Show admin history for a user."
    )
    await update.message.reply_text(text, parse_mode="Markdown")


@founder_required
async def panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    text = (
        "🔒 **Edward Admin Panel**\n\n"
        f"🌐 Global Bans: `{len(db.get('gbans', []))}`\n"
        f"🤝 Federation Bans: `{len(db.get('fbans', []))}`\n"
        f"👑 Whitelist Founders: `{len(founders_list())}`\n"
        f"🏰 Enforced Groups: `{len(db.get('enforced_groups', []))}`\n"
        f"📡 Federation Groups: `{len(db.get('federation_groups', []))}`\n\n"
        f"✅ System Mode: `{'Secure' if db.get('secure_mode', True) else 'Open'}`"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


@founder_required
async def addfounder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /addfounder <user_id>")
        return

    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return

    if uid in PERMANENT_FOUNDERS:
        await update.message.reply_text("User is already a permanent founder.")
        return

    dyn = set(db.get("founders_dynamic", []))
    dyn.add(uid)
    db["founders_dynamic"] = list(dyn)
    save_db(db)
    await update.message.reply_text(f"✅ Added founder: {uid}")


@founder_required
async def removefounder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /removefounder <user_id>")
        return

    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return

    if uid in PERMANENT_FOUNDERS:
        await update.message.reply_text("⛔ Cannot remove a permanent founder.")
        return

    dyn = set(db.get("founders_dynamic", []))
    if uid in dyn:
        dyn.remove(uid)
        db["founders_dynamic"] = list(dyn)
        save_db(db)
        await update.message.reply_text(f"✅ Removed founder: {uid}")
    else:
        await update.message.reply_text("User is not a dynamic founder.")


@founder_required
async def founders_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    fl = founders_list()
    await update.message.reply_text("👑 Founders:\n" + "\n".join(f"- {x}" for x in fl))


@founder_required
async def secure_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /secure on|off")
        return
    mode = context.args[0].lower()
    if mode not in ("on", "off"):
        await update.message.reply_text("Usage: /secure on|off")
        return
    db["secure_mode"] = mode == "on"
    save_db(db)
    await update.message.reply_text(f"🔒 Secure mode set to: {db['secure_mode']}")


# ─────────────────────────────────────────────────────────────
# Shadowban System
# ─────────────────────────────────────────────────────────────
@founder_required
async def shadowban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /shadowban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    sb = set(db.get("shadowbans", []))
    sb.add(uid)
    db["shadowbans"] = list(sb)
    save_db(db)
    await update.message.reply_text(f"✅ Shadowbanned {uid}. Their messages will be deleted silently.")


@founder_required
async def unshadowban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /unshadowban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except ValueError:
        await update.message.reply_text("Invalid user ID.")
        return
    sb = set(db.get("shadowbans", []))
    if uid in sb:
        sb.remove(uid)
        db["shadowbans"] = list(sb)
        save_db(db)
        await update.message.reply_text(f"✅ Unshadowbanned {uid}.")
    else:
        await update.message.reply_text("User is not shadowbanned.")


# ─────────────────────────────────────────────────────────────
# Message Filtering
# ─────────────────────────────────────────────────────────────
async def on_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return
    user = msg.from_user
    chat = msg.chat
    db = load_db()

    if not user:
        return

    # Skip founders
    if user.id in PERMANENT_FOUNDERS:
        return

    # Shadowban enforcement
    if user.id in db.get("shadowbans", []) and chat.type in ("group", "supergroup"):
        try:
            await msg.delete()
        except Exception as e:
            log.warning("Failed to delete message: %s", e)
        return


# ─────────────────────────────────────────────────────────────
# Bot Entry Point
# ─────────────────────────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # General
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))

    # Founder-only
    app.add_handler(CommandHandler("panel", panel))
    app.add_handler(CommandHandler("status", panel))
    app.add_handler(CommandHandler("addfounder", addfounder))
    app.add_handler(CommandHandler("removefounder", removefounder))
    app.add_handler(CommandHandler("founders", founders_cmd))
    app.add_handler(CommandHandler("secure", secure_cmd))
    app.add_handler(CommandHandler("shadowban", shadowban))
    app.add_handler(CommandHandler("unshadowban", unshadowban))

    # Message monitor
    app.add_handler(MessageHandler(filters.ALL, on_message))

    log.info("✅ Edward Admin Bot started and running...")
    app.run_polling()


if __name__ == "__main__":
    main()
