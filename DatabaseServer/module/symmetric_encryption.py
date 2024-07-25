import csv
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os
import hashlib

router = APIRouter()

# Get the absolute path of the current script's directory
module_dir = os.path.dirname(__file__)

# Construct the path to config.json
config_path = os.path.join(module_dir, '..', 'config.json')

# Read config.json
with open(config_path, 'r') as f:
    config = json.load(f)

database_node = config['database_symmetric_encryption']
database_password = config['database_password']

def read_csv(filepath: str) -> list:
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def write_csv(filepath: str, data: list):
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['id', 'encryption']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/update_symmetric_encryption/")
async def update_encryption(request: Request):
    node = await request.json()
    required_fields = {"id", "encryption", "password"}

    provided_id = node.get('id')
    provided_password = node.get('password')
    
    if not provided_id or not provided_password:
        raise HTTPException(status_code=400, detail="ID and password required")
    
    hashed_password = hash_password(provided_password)

    # Check the provided ID and hashed password
    try:
        data_password = read_csv(database_password)
        valid_credentials = any(
            row['id'] == provided_id and row['password'] == hashed_password
            for row in data_password
        )

        if not valid_credentials:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not required_fields.issubset(node.keys()):
            raise HTTPException(status_code=400, detail="Missing required fields")

        data = read_csv(database_node)
        updated = False

        for row in data:
            if row['id'] == str(node['id']) and row['encryption'] == node['encryption']:
                # If a row with the same id and encryption is found, do nothing
                updated = True
                break

        node.pop('password', None)
        if not updated:
            data.append(node)

        write_csv(database_node, data)
        return {"message": "Encryption added or updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the CSV file: {str(e)}")

@router.post("/remove_symmetric_encryption/")
async def remove_encryption(request: Request):
    node = await request.json()
    required_fields = {"id", "encryption", "password"}

    provided_id = node.get('id')
    provided_password = node.get('password')
    
    if not provided_id or not provided_password:
        raise HTTPException(status_code=400, detail="ID and password required")
    
    hashed_password = hash_password(provided_password)

    # Check the provided ID and hashed password
    try:
        data_password = read_csv(database_password)
        valid_credentials = any(
            row['id'] == provided_id and row['password'] == hashed_password
            for row in data_password
        )

        if not valid_credentials:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        if not required_fields.issubset(node.keys()):
            raise HTTPException(status_code=400, detail="Missing required fields")

        data = read_csv(database_node)
        removed = False

        for idx, row in enumerate(data):
            if row['id'] == str(node['id']) and row['encryption'] == node['encryption']:
                del data[idx]
                removed = True
                break

        if not removed:
            raise HTTPException(status_code=404, detail="Encryption entry not found")

        write_csv(database_node, data)
        return {"message": "Encryption removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the CSV file: {str(e)}")