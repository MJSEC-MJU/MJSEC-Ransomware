import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def decrypt_file(encrypted_path, original_path, key, iv):
    try:
        with open(encrypted_path, "rb") as f:
            encrypted_data = f.read()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        with open(original_path, "wb") as f:
            f.write(data)

        os.remove(encrypted_path)
        print(f"[+] Decrypted {encrypted_path}")

    except Exception as e:
        print(f"[!] Decryption failed: {e}")
        raise e

def clean_deleted_records(meta_path):
    if not os.path.exists(meta_path):
        return

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)
    except Exception:
        return

    new_meta = {k: v for k, v in meta.items() if not (isinstance(v, dict) and v.get("deleted"))}

    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(new_meta, f, indent=2)
    except Exception:
        pass