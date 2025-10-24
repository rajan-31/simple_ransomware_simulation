# Ransomware Simulation

This project demonstrates encryption and decryption using symmetric key cryptography. THe experiments involve encryption and decryption on varying number of files, decryption with wrong key, decryption of corrupted files.

## Overview

The script simulates four key stages of ransomware-like behavior:

1. **create** – Generates sample files in a test folder.
2. **encrypt** – Encrypts those files using symmetric encryption (Fernet/AES).
3. **decrypt** – Decrypts the files back using the stored key.
4. **clean** – Safely deletes the test data while keeping logs.

Each step logs detailed information such as timestamps, execution time, progress, and file details into a CSV log file.

## Folder Structure (after running create action first time)

```
ransomware_sim_test/
├── original/           # Sample files created by the script
├── encrypted/          # Encrypted versions (.enc)
├── decrypted/          # Decrypted output for verification
├── manifest.csv        # Records original/encrypted/decrypted hashes
├── symmetric.key       # Encryption key used for Fernet
├── actions_log.csv     # All operations are logged here
└── .gitkeep            # For version control safety
```

## Usage

Create and activate python environment

```bash
python3 -m venv .venv
source .ven/bin/activate
```

Install dependencies

```bash
pip3 install -r requirements.txt
```

Run the script with one of the supported actions:

```bash
python3 safe_ransom_sim_simple.py --action create
python3 safe_ransom_sim_simple.py --action encrypt
python3 safe_ransom_sim_simple.py --action decrypt
python3 safe_ransom_sim_simple.py --action clean
```

### Example Workflow

1. **Create**: Generates a few test files (text, CSV, binary).
2. **Encrypt**: Encrypts the test files, saves `.enc` versions, and writes a manifest.
3. **Decrypt**: Decrypts `.enc` files and verifies hashes to ensure integrity.
4. **Clean**: Deletes all test data except for logs and `.gitkeep`.

## Internals

* **Encryption:** Uses `cryptography.Fernet`, which internally applies AES-128 in CBC mode with HMAC authentication.
* **Hashing:** SHA-256 is used to verify data integrity before and after decryption.
* **Logging:** All operations are timestamped in Indian Standard Time (IST) using ISO 8601 format (e.g. `2025-10-24T20:12:32+05:30`).
* **Safety:** The script only operates inside the `ransomware_sim_test` directory to ensure no external files are affected.

## Example Log Entry

| action  | start_time                | time_total(s) | files_count | total_size(KB) | progress_percent | notes                            |
| ------- | ------------------------- | ------------- | ----------- | -------------- | ---------------- |----------------------------------|
| encrypt | 2025-10-24T20:12:32+05:30 | 0.041         | 3           | 1.62           | 100.0            | Exp 100 - simple encryption test |