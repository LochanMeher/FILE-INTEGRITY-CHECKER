import hashlib
import os
import json

# Path to store baseline hash values
BASELINE_FILE = "file_hashes.json"

def calculate_file_hash(filepath):
    """Calculate the SHA-256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None

def generate_baseline(directory):
    """Generate a baseline hash record for all files in a directory."""
    hash_dict = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            hash_dict[filepath] = calculate_file_hash(filepath)
    
    with open(BASELINE_FILE, "w") as f:
        json.dump(hash_dict, f, indent=4)
    
    print("Baseline hashes generated and saved.")

def check_integrity():
    """Check the integrity of files by comparing current hashes with baseline."""
    if not os.path.exists(BASELINE_FILE):
        print("Baseline file not found. Generate it first with 'generate_baseline()'.")
        return
    
    with open(BASELINE_FILE, "r") as f:
        old_hashes = json.load(f)

    for filepath, old_hash in old_hashes.items():
        current_hash = calculate_file_hash(filepath)
        if current_hash is None:
            print(f"File missing: {filepath}")
        elif current_hash != old_hash:
            print(f"Integrity breach detected: {filepath}")
        else:
            print(f"File OK: {filepath}")

def main():
    print("File Integrity Checker")
    print("1. Generate baseline")
    print("2. Check file integrity")
    choice = input("Enter your choice (1 or 2): ")

    directory = input("Enter the directory path to scan: ")

    if choice == '1':
        generate_baseline(directory)
    elif choice == '2':
        check_integrity()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()