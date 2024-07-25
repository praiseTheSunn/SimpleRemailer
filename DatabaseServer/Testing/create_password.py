import csv
import json
import hashlib
import os

# Get the absolute path of the current script's directory
module_dir = os.path.dirname(__file__)

# Construct the path to config.json
config_path = os.path.join(module_dir, '..', 'config.json')

# Read config.json
with open(config_path, 'r') as f:
    config = json.load(f)

database_password = config['database_password']
print(database_password)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def update_passwords(filepath: str):
    temp_file = filepath + '.tmp'

    with open(filepath, 'r', newline='') as infile, open(temp_file, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames

        # Check if 'id' and 'password' fields are present
        if 'id' not in fieldnames or 'password' not in fieldnames:
            raise ValueError("CSV file must contain 'id' and 'password' columns")

        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # Hash the password
            row['password'] = hash_password(row['password'])
            writer.writerow(row)

    # Replace old file with new file
    os.replace(temp_file, filepath)
    print("Passwords have been updated and file saved.")

update_passwords(database_password)
