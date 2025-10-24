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

| action | start_time                  | time_total(s) | files_count | total_size(KB) | progress_percent | notes                           |
|--------|-----------------------------|---------------|-------------|----------------|------------------|---------------------------------|
| encrypt| 2025-10-24T20:42:37.389893+05:30 | 0.136        | 100         | 15964196       | 100.0            | Exp 01 - test encryption for 100 files

## Example Manifest

| filename              | orig_hash                                                                 | encrypted_name            | encrypted_size | decrypted_hash | status    |
|-----------------------|---------------------------------------------------------------------------|---------------------------|----------------|----------------|-----------|
| data.csv              | d8066f036c8080cdcb9b2ae93a5c9cde775a6bfce0571170e13f5114c787c58a | data.csv.enc              | 120            |                | encrypted |
| image_placeholder.bin | 0a56e62055eb2aff8fe9807836abb20dbb66b0b6e1c2a06e3266572933ad4ab1 | image_placeholder.bin.enc | 780            |                | encrypted |
| notes.txt             | 081d2583dc1497b444cf40b92a553002225dd93797f05a44ef3947fa44380a6e | notes.txt.enc             | 184            |                | encrypted

| filename              | orig_hash                                                                 | encrypted_name            | encrypted_size | decrypted_hash                                                                 | status        |
|-----------------------|---------------------------------------------------------------------------|---------------------------|----------------|-------------------------------------------------------------------------------|---------------|
| data.csv              | d8066f036c8080cdcb9b2ae93a5c9cde775a6bfce0571170e13f5114c787c58a | data.csv.enc              | 120            | d8066f036c8080cdcb9b2ae93a5c9cde775a6bfce0571170e13f5114c787c58a | decrypted_ok |
| image_placeholder.bin | 0a56e62055eb2aff8fe9807836abb20dbb66b0b6e1c2a06e3266572933ad4ab1 | image_placeholder.bin.enc | 780            | 0a56e62055eb2aff8fe9807836abb20dbb66b0b6e1c2a06e3266572933ad4ab1 | decrypted_ok |
| notes.txt             | 081d2583dc1497b444cf40b92a553002225dd93797f05a44ef3947fa44380a6e | notes.txt.enc             | 184            | 081d2583dc1497b444cf40b92a553002225dd93797f05a44ef3947fa44380a6e | decrypted_ok