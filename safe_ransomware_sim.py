#!/usr/bin/env python3
"""
Features
  - create   : create sample files in the test folder
  - encrypt  : encrypt those sample files (writes .enc files)
  - decrypt  : decrypt using the stored key (writes decrypted files)
  - clean    : delete the entire test folder

Usage examples:
  python3 safe_ransom_sim_simple.py --action create
  python3 safe_ransom_sim_simple.py --action encrypt
  python3 safe_ransom_sim_simple.py --action decrypt
  python3 safe_ransom_sim_simple.py --action clean
"""

import argparse
import shutil
import os
import hashlib
import csv
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from cryptography.fernet import Fernet

# ----- Configuration -----
BASE = Path("ransomware_sim_test")
SAMPLE_DIR = BASE / "original"
ENCRYPTED_DIR = BASE / "encrypted"
DECRYPTED_DIR = BASE / "decrypted"
MANIFEST = BASE / "manifest.csv"
KEY_FILE = BASE / "symmetric.key"
LOG_FILE = BASE / "actions_log.csv"

IST = timezone(timedelta(hours=5, minutes=30))

# ---------------------------------------------------------

def ensure_dirs():
    BASE.mkdir(exist_ok=True)
    SAMPLE_DIR.mkdir(exist_ok=True)
    ENCRYPTED_DIR.mkdir(exist_ok=True)
    DECRYPTED_DIR.mkdir(exist_ok=True)

def sha256(path: Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()

def log_action(action, start_time, time_total=None, files_count=None, total_size=None, progress=None, notes=""):
    ensure_dirs()
    newfile = not LOG_FILE.exists()
    with LOG_FILE.open("a", newline="") as lf:
        writer = csv.DictWriter(lf, fieldnames=["action", "start_time", "time_total", "files_count", "total_size", "progress_percent", "notes"])
        if newfile:
            writer.writeheader()
        writer.writerow({
            "action": action,
            "start_time": start_time,
            "time_total": f"{time_total:.3f}" if time_total is not None else "",
            "files_count": files_count if files_count is not None else "",
            "total_size": total_size if total_size is not None else "",
            "progress_percent": f"{progress:.1f}" if progress is not None else "",
            "notes": notes
        })

def action_create():
    start = time.time()
    ensure_dirs()
    # sample files
    (SAMPLE_DIR / "notes.txt").write_text(
        "This is a sample text file for encryption simulation.\nDo not use real data."
    )
    (SAMPLE_DIR / "data.csv").write_text("id,value\n1,100\n2,200\n3,300\n")
    (SAMPLE_DIR / "image_placeholder.bin").write_bytes(os.urandom(512))
    print(f"[create] Created sample files in: {SAMPLE_DIR.resolve()}")
    log_action("create", datetime.now(IST).isoformat(), time.time()-start)

def load_or_generate_key():
    ensure_dirs()
    if KEY_FILE.exists():
        key = KEY_FILE.read_bytes()
        print(f"[key] Loaded existing key from {KEY_FILE}")
    else:
        key = Fernet.generate_key()
        KEY_FILE.write_bytes(key)
        print(f"[key] Generated new key and saved to {KEY_FILE}")
    return Fernet(key)

def action_encrypt():
    start = time.time()
    ensure_dirs()
    f = load_or_generate_key()
    rows = []
    files = sorted([p for p in SAMPLE_DIR.iterdir() if p.is_file()])
    if not files:
        print("[encrypt] No sample files found. Run --action create first.")
        return

    total_size = 0
    success = 0

    for p in files:
        try:
            orig_hash = sha256(p)
            token = f.encrypt(p.read_bytes())
            out = ENCRYPTED_DIR / (p.name + ".enc")
            out.write_bytes(token)
            total_size += out.stat().st_size
            rows.append({
                "filename": p.name,
                "orig_hash": orig_hash,
                "encrypted_name": out.name,
                "encrypted_size": out.stat().st_size,
                "decrypted_hash": "",
                "status": "encrypted"
            })
            success += 1
            print(f"[encrypt] {p.name} -> {out.name}")
        except Exception as e:
            print(f"[encrypt] Failed: {p.name} ({e})")

    with MANIFEST.open("w", newline="") as mf:
        writer = csv.DictWriter(mf, fieldnames=["filename","orig_hash","encrypted_name","encrypted_size","decrypted_hash","status"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"[encrypt] Manifest written to {MANIFEST}")

    progress = (success / len(files)) * 100
    log_action("encrypt", datetime.now(IST).isoformat(), time.time()-start, len(files), total_size, progress)

def action_decrypt():
    start = time.time()
    ensure_dirs()
    if not KEY_FILE.exists():
        print("[decrypt] Error: key file not found. Run --action encrypt first.")
        return
    if not MANIFEST.exists():
        print("[decrypt] Error: manifest not found. Run --action encrypt first.")
        return
    f = load_or_generate_key()
    updated = []
    total_size = 0
    success = 0
    with MANIFEST.open("r", newline="") as mf:
        reader = csv.DictReader(mf)
        for row in reader:
            enc_path = ENCRYPTED_DIR / row["encrypted_name"]
            try:
                token = enc_path.read_bytes()
                plaintext = f.decrypt(token)
                out = DECRYPTED_DIR / row["filename"]
                out.write_bytes(plaintext)
                total_size += out.stat().st_size
                dec_hash = sha256(out)
                row["decrypted_hash"] = dec_hash
                row["status"] = "decrypted_ok" if dec_hash == row["orig_hash"] else "decrypted_mismatch"
                print(f"[decrypt] {enc_path.name} -> {out.name} ({row['status']})")
                if row["status"] == "decrypted_ok":
                    success += 1
            except Exception as e:
                row["status"] = f"decrypt_error: {e}"
                print(f"[decrypt] Failed to decrypt {row.get('encrypted_name','?')}: {e}")
            updated.append(row)

    with MANIFEST.open("w", newline="") as mf:
        writer = csv.DictWriter(mf, fieldnames=["filename","orig_hash","encrypted_name","encrypted_size","decrypted_hash","status"])
        writer.writeheader()
        for r in updated:
            writer.writerow(r)
    print(f"[decrypt] Manifest updated at {MANIFEST}")

    progress = (success / len(updated)) * 100 if updated else 0
    log_action("decrypt", datetime.now(IST).isoformat(), time.time()-start, len(updated), total_size, progress)

def action_clean():
    start = time.time()
    if BASE.exists():
        shutil.rmtree(BASE)
        print(f"[clean] Removed test folder: {BASE.resolve()}")
    else:
        print("[clean] Nothing to remove.")
    log_action("clean", datetime.now(IST).isoformat(), time.time()-start)

def parse_args():
    p = argparse.ArgumentParser(description="Safe ransomware simulation.")
    p.add_argument("--action", required=True, choices=["create","encrypt","decrypt","clean"], help="Single action to perform")
    return p.parse_args()

def main():
    args = parse_args()
    a = args.action
    print(f"[main] Action: {a}")
    if a == "create":
        action_create()
    elif a == "encrypt":
        action_encrypt()
    elif a == "decrypt":
        action_decrypt()
    elif a == "clean":
        action_clean()
    else:
        print("[main] Unknown action (this should not occur).")

if __name__ == "__main__":
    main()
