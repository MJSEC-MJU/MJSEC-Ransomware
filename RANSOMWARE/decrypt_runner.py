import os
import json
from decryptor import decrypt_file

META_PATH = "encryption_meta.json"

def decrypt_all_files(id_str):
    if not os.path.exists(META_PATH):
        print("[!] Meta file not found")
        return

    with open(META_PATH, "r", encoding="utf-8") as f:
        meta = json.load(f)

    changed = False

    for encrypted_path, info in meta.items():
        if not isinstance(info, dict):
            print(f"[!] Meta info for {encrypted_path} is not dict, skipping")
            continue

        if info.get("deleted", False):
            continue

        original_path = info.get("original_path")
        key_hex = info.get("key")
        iv_hex = info.get("iv")

        if not all([original_path, key_hex, iv_hex]):
            print(f"[!] Meta info incomplete for {encrypted_path}, skipping")
            continue

        try:
            key = bytes.fromhex(key_hex)
            iv = bytes.fromhex(iv_hex)
            decrypt_file(encrypted_path, original_path, key, iv)
            info["deleted"] = True
            changed = True
        except Exception as e:
            print(f"[!] Failed to decrypt {encrypted_path}: {e}")

    if changed:
        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
