import logging, datetime
from utils.db_utils import load_db, save_db

LOG_FILE = "event_logs.txt"
logging.basicConfig(level=logging.INFO)
log = logging.getLogger("EdwardBot")

def log_action(user_id, action, admin_id):
    db = load_db()
    history = db.get("history", {})
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{ts}] {action} by admin {admin_id}"
    user_hist = history.get(str(user_id), [])
    user_hist.append(entry)
    history[str(user_id)] = user_hist[-20:]
    db["history"] = history
    save_db(db)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{ts}] USER:{user_id} | ACTION:{action} | ADMIN:{admin_id}\n")
