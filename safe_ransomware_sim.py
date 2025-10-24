#!/usr/bin/env python3

import argparse
import os
from pathlib import Path

# Configuration
BASE = Path("ransomware_sim_test")
SAMPLE_DIR = BASE / "original"

def ensure_dirs():
    BASE.mkdir(exist_ok=True)
    SAMPLE_DIR.mkdir(exist_ok=True)

def action_create():
    ensure_dirs()
    # Create sample files
    (SAMPLE_DIR / "notes.txt").write_text(
        "This is a sample text file for encryption simulation.\nDo not use real data."
    )
    (SAMPLE_DIR / "data.csv").write_text("id,value\n1,100\n2,200\n3,300\n")
    (SAMPLE_DIR / "image_placeholder.bin").write_bytes(os.urandom(512))
    print(f"[create] Created sample files in: {SAMPLE_DIR.resolve()}")

def parse_args():
    p = argparse.ArgumentParser(description="Safe ransomware simulation.")
    p.add_argument("--action", required=True, choices=["create"], help="Action to perform")
    return p.parse_args()

def main():
    args = parse_args()
    if args.action == "create":
        action_create()

if __name__ == "__main__":
    main()