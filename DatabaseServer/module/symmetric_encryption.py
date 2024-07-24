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

database_node = config['database_symmetric_encryption']
