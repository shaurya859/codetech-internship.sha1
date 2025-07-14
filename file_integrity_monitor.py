import os
import hashlib
import json

HASH_RECORD_FILE = 'file_hashes.json'

def get_file_hash(file_path):
    sha256 = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except FileNotFoundError:
        return None

def scan_directory(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            full_path = os.path.join(root, file)
            hash_value = get_file_hash(full_path)
            if hash_value:
                file_hashes[full_path] = hash_value
    return file_hashes

def load_previous_hashes():
    if os.path.exists(HASH_RECORD_FILE):
        with open(HASH_RECORD_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_hashes(hashes):
    with open(HASH_RECORD_FILE, 'w') as f:
        json.dump(hashes, f, indent=2)

def compare_hashes(old_hashes, new_hashes):
    old_files = set(old_hashes)
    new_files = set(new_hashes)

    added = new_files - old_files
    removed = old_files - new_files
    modified = {file for file in old_files & new_files if old_hashes[file] != new_hashes[file]}

    return added, removed, modified

def main():
    path = input("Enter directory path to monitor: ").strip()
    print(f"\n🔍 Scanning '{path}'...\n")

    current_hashes = scan_directory(path)
    previous_hashes = load_previous_hashes()

    added, removed, modified = compare_hashes(previous_hashes, current_hashes)

    print("📂 Changes Detected:\n")
    if added:
        print("🟢 Added Files:")
        for file in added:
            print("  +", file)
    if removed:
        print("🔴 Removed Files:")
        for file in removed:
            print("  -", file)
    if modified:
        print("🟡 Modified Files:")
        for file in modified:
            print("  *", file)
    if not (added or removed or modified):
        print("✅ No changes detected.")

    save_hashes(current_hashes)

if __name__ == "__main__":
    main()
