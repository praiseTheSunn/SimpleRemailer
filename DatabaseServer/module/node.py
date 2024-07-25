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

database_node = config['database_node']
database_name = config['database_name']
database_symmetric_encryption = config['database_symmetric_encryption']
database_password = config['database_password']

def read_csv(filepath: str) -> list:
    with open(filepath, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def verify_credentials(id: str, password: str) -> bool:
    data_password = read_csv(database_password)
    for row in data_password:
        if row['id'] == id and row['password'] == password:
            return True
    return False

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

@router.post("/get_list_node")
async def get_list_node(request: Request):
    body = await request.json()
    provided_id = body.get('id')
    provided_password = body.get('password')
    
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

        data_name = read_csv(database_name)
        data_node = read_csv(database_node)
        data_symmetric_encryption = read_csv(database_symmetric_encryption)

        # Create a dictionary to store data by id
        node_data = {}

        # Process data_name for basic info
        for row in data_name:
            node_id = row['id']
            node_data[node_id] = {
                'id': node_id,
                'nickname': row.get('nickname', ''),
                'status': row.get('status', ''),
                'asymmetric_encryptions': [],
                'symmetric_encryptions': []
            }

        # Process data_node for asymmetric encryption and public keys
        for row in data_node:
            node_id = row['id']
            if node_id in node_data:
                node_data[node_id]['asymmetric_encryptions'].append({
                    'encryption': row.get('encryption', ''),
                    'public_key': row.get('public_key', '')
                })

        # Process data_symmetric_encryption for symmetric encryption methods
        for row in data_symmetric_encryption:
            node_id = row['id']
            if node_id in node_data:
                node_data[node_id]['symmetric_encryptions'].append(row.get('encryption', ''))

        # Convert the node_data dict to a list
        result = list(node_data.values())

        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the CSV file: {str(e)}")

@router.post("/get_list_available_node")
async def get_list_available_node(request: Request):
    body = await request.json()
    provided_id = body.get('id')
    provided_password = body.get('password')
    
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

        data_name = read_csv(database_name)
        data_node = read_csv(database_node)
        data_symmetric_encryption = read_csv(database_symmetric_encryption)

        # Create a dictionary to store data by id
        node_data = {}

        # Process data_name for basic info and filter by status
        for row in data_name:
            if row.get('status') == '0':  # Check if the status is '0'
                node_id = row['id']
                node_data[node_id] = {
                    'id': node_id,
                    'nickname': row.get('nickname', ''),
                    'status': row.get('status', ''),
                    'asymmetric_encryptions': [],
                    'symmetric_encryptions': []
                }

        # Process data_node for asymmetric encryption and public keys
        for row in data_node:
            node_id = row['id']
            if node_id in node_data:
                node_data[node_id]['asymmetric_encryptions'].append({
                    'encryption': row.get('encryption', ''),
                    'public_key': row.get('public_key', '')
                })

        # Process data_symmetric_encryption for symmetric encryption methods
        for row in data_symmetric_encryption:
            node_id = row['id']
            if node_id in node_data:
                node_data[node_id]['symmetric_encryptions'].append(row.get('encryption', ''))

        # Convert the node_data dict to a list
        result = list(node_data.values())

        return JSONResponse(content=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the CSV file: {str(e)}")
