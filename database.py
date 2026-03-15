users = {}
scores = {}

def add_user(user_id):
    if user_id not in users:
        users[user_id] = {"paid": False}

def is_paid(user_id):
    return users.get(user_id, {}).get("paid", False)

def activate(user_id):
    users[user_id]["paid"] = True

def save_score(user_id, score):
    scores[user_id] = score
