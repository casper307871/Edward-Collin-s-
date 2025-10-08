from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from utils.db_utils import load_db, save_db, is_protected
from utils.logger import log_action
from utils.protection import rescue_protected_user

async def gban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /gban <user_id> [reason]")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if is_protected(uid):
        await update.message.reply_text("⛔ User is protected. GBAN blocked.")
        log_action(uid, "Attempted GBAN on protected user", update.effective_user.id)
        return
    db["gbans"].append(uid)
    db["gbans"] = list(set(db["gbans"]))
    save_db(db)
    log_action(uid, "GBAN applied", update.effective_user.id)
    await update.message.reply_text(f"✅ GBAN applied: {uid}")

async def ungban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /ungban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if uid in db.get("gbans", []):
        db["gbans"].remove(uid)
        save_db(db)
        log_action(uid, "GBAN removed", update.effective_user.id)
        await update.message.reply_text(f"✅ GBAN removed: {uid}")
    else:
        await update.message.reply_text("User not GBANned.")

async def fban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /fban <user_id> [reason]")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if is_protected(uid):
        await update.message.reply_text("⛔ User is protected. FBAN blocked.")
        log_action(uid, "Attempted FBAN on protected user", update.effective_user.id)
        return
    db["fbans"].append(uid)
    db["fbans"] = list(set(db["fbans"]))
    save_db(db)
    log_action(uid, "FBAN applied", update.effective_user.id)
    await update.message.reply_text(f"✅ FBAN applied: {uid}")

async def unfban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /unfban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if uid in db.get("fbans", []):
        db["fbans"].remove(uid)
        save_db(db)
        log_action(uid, "FBAN removed", update.effective_user.id)
        await update.message.reply_text(f"✅ FBAN removed: {uid}")
    else:
        await update.message.reply_text("User not FBANned.")

async def shadowban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /shadowban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if is_protected(uid):
        await update.message.reply_text("⛔ User is protected. Shadowban blocked.")
        log_action(uid, "Attempted shadowban on protected user", update.effective_user.id)
        return
    sb = set(db.get("shadowbans", []))
    sb.add(uid)
    db["shadowbans"] = list(sb)
    save_db(db)
    log_action(uid, "Shadowban applied", update.effective_user.id)
    await update.message.reply_text(f"✅ Shadowbanned {uid}")

async def unshadowban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /unshadowban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    sb = set(db.get("shadowbans", []))
    if uid in sb:
        sb.remove(uid)
        db["shadowbans"] = list(sb)
        save_db(db)
        log_action(uid, "Shadowban removed", update.effective_user.id)
        await update.message.reply_text(f"✅ Unshadowbanned {uid}")
    else:
        await update.message.reply_text("User is not shadowbanned.")

async def casban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # CASBAN: Remove admin + ban in all enforced groups
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /casban <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    if is_protected(uid):
        await update.message.reply_text("⛔ User is protected. CASBAN blocked.")
        log_action(uid, "Attempted CASBAN on protected user", update.effective_user.id)
        return
    for gid in db.get("enforced_groups", []):
        try:
            await context.bot.promote_chat_member(gid, uid, can_manage_chat=False, can_delete_messages=False)
            await context.bot.ban_chat_member(gid, uid)
        except:
            pass
    log_action(uid, "CASBAN applied", update.effective_user.id)
    await update.message.reply_text(f"✅ CASBAN applied to {uid}")

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /protect <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    protected = set(db.get("protected_users", []))
    protected.add(uid)
    db["protected_users"] = list(protected)
    save_db(db)
    log_action(uid, "User protected", update.effective_user.id)
    await update.message.reply_text(f"✅ User {uid} is now protected")

async def unprotect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    if not context.args:
        await update.message.reply_text("Usage: /unprotect <user_id>")
        return
    try:
        uid = int(context.args[0])
    except:
        await update.message.reply_text("Invalid user id.")
        return
    protected = set(db.get("protected_users", []))
    if uid in protected:
        protected.remove(uid)
        db["protected_users"] = list(protected)
        save_db(db)
        log_action(uid, "User unprotected", update.effective_user.id)
        await update.message.reply_text(f"✅ User {uid} is no longer protected")
    else:
        await update.message.reply_text("User was not protected")

async def protectedlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = load_db()
    plist = db.get("protected_users", [])
    await update.message.reply_text("Protected users: " + ", ".join(str(x) for x in plist))
