#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
from cryptography.fernet import Fernet

# Configuration
BASE = Path("ransomware_sim_test")
SAMPLE_DIR = BASE / "original"
ENCRYPTED_DIR = BASE / "encrypted"
KEY_FILE = BASE / "symmetric.key"

def ensure_dirs():
    BASE.mkdir(exist_ok=True)
    SAMPLE_DIR.mkdir(exist_ok=True)
    ENCRYPTED_DIR.mkdir(exist_ok=True)

def action_create():
    ensure_dirs()
    (SAMPLE_DIR / "notes.txt").write_text(
        "This is a sample text file for encryption simulation.\nDo not use real data."
    )
    (SAMPLE_DIR / "data.csv").write_text("id,value\n1,100\n2,200\n3,300\n")
    (SAMPLE_DIR / "image_placeholder.bin").write_bytes(os.urandom(512))
    print(f"[create] Created sample files in: {SAMPLE_DIR.resolve()}")

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
    ensure_dirs()
    f = load_or_generate_key()
    files = sorted([p for p in SAMPLE_DIR.iterdir() if p.is_file()])
    if not files:
        print("[encrypt] No sample files found. Run --action create first.")
        return
    for p in files:
        token = f.encrypt(p.read_bytes())
        out = ENCRYPTED_DIR / (p.name + ".enc")
        out.write_bytes(token)
        print(f"[encrypt] {p.name} -> {out.name}")

def parse_args():
    p = argparse.ArgumentParser(description="Safe ransomware simulation.")
    p.add_argument("--action", required=True, choices=["create", "encrypt"], help="Action to perform")
    return p.parse_args()

def main():
    args = parse_args()
    if args.action == "create":
        action_create()
    elif args.action == "encrypt":
        action_encrypt()

if __name__ == "__main__":
    main()