import json, os

DATA_FILE = "data.json"

def load_db():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({
                "founders_dynamic": [],
                "gbans": [],
                "fbans": [],
                "enforced_groups": [],
                "federation_groups": [],
                "secure_mode": True,
                "shadowbans": [],
                "protected_users": [],
                "history": {},
                "auto_enforce": True
            }, f, indent=2)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_db(db):
    with open(DATA_FILE, "w") as f:
        json.dump(db, f, indent=2)

def preload_enforced_groups(initial_groups):
    db = load_db()
    current = set(db.get("enforced_groups", []))
    db["enforced_groups"] = list(current.union(initial_groups))
    save_db(db)

def is_founder(user_id, PERMANENT_FOUNDERS):
    db = load_db()
    return user_id in PERMANENT_FOUNDERS or user_id in db.get("founders_dynamic", [])

def is_protected(user_id):
    db = load_db()
    return user_id in db.get("protected_users", [])
