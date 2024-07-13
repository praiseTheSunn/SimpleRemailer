# module/encryption.py
import csv
import json
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
import os

router = APIRouter()

# Get the absolute path of the current script's directory
module_dir = os.path.dirname(__file__)

# Construct the path to config.json
config_path = os.path.join(module_dir, '..', 'config.json')

# Read config.json
with open(config_path, 'r') as f:
    config = json.load(f)

database_node = config['database_node']

def read_csv(filepath: str) -> list:
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def write_csv(filepath: str, data: list):
    with open(filepath, 'w', newline='') as csvfile:
        fieldnames = ['id', 'ip', 'encryption', 'public_key']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

@router.post("/update_encryption/")
async def update_encryption(request: Request):
    node = await request.json()
    required_fields = {"id", "ip", "encryption", "public_key"}

    # print(type(node))
    # return 

    if not required_fields.issubset(node.keys()):
        raise HTTPException(status_code=400, detail="Missing required fields")

    data = read_csv(database_node)
    updated = False

    for row in data:
        if row['id'] == str(node['id']) and row['ip'] == node['ip'] and row['encryption'] == node['encryption']:
            row['public_key'] = node['public_key']
            updated = True
            break

    if not updated:
        data.append(node)

    write_csv(database_node, data)
    return {"message": "Encryption added or updated successfully"}

@router.post("/remove_encryption/")
async def remove_encryption(request: Request):
    node = await request.json()
    required_fields = {"id", "ip", "encryption"}

    if not required_fields.issubset(node.keys()):
        raise HTTPException(status_code=400, detail="Missing required fields")

    data = read_csv(database_node)
    removed = False

    for idx, row in enumerate(data):
        if row['id'] == str(node['id']) and row['ip'] == node['ip'] and row['encryption'] == node['encryption']:
            del data[idx]
            removed = True
            break

    if not removed:
        raise HTTPException(status_code=404, detail="Encryption entry not found")

    write_csv(database_node, data)
    return {"message": "Encryption removed successfully"}

@router.get("/get_encryption")
async def get_encryption():
    try:
        data = read_csv(database_node)
        return JSONResponse(content=data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the CSV file: {str(e)}")
