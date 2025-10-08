from utils.db_utils import is_protected
from utils.logger import log_action
from telegram import ChatPermissions

async def rescue_protected_user(bot, chat_id, user_id):
    if not is_protected(user_id):
        return
    try:
        member = await bot.get_chat_member(chat_id, user_id)
        if member.status in ["kicked", "left"]:
            await bot.unban_chat_member(chat_id, user_id)
            log_action(user_id, "Protected user unbanned/rescued", 0)
        elif hasattr(member, "can_send_messages") and member.can_send_messages is False:
            await bot.restrict_chat_member(chat_id, user_id, permissions=ChatPermissions(can_send_messages=True))
            log_action(user_id, "Protected user unmuted automatically", 0)
    except Exception as e:
        log_action(user_id, f"Failed rescue: {e}", 0)
