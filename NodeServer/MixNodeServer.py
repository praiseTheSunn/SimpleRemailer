from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os
import json

config_file = os.path.join(os.path.dirname(__file__), "Storage", "config.json")
with open(config_file, 'r') as file:
    data = json.load(file)
ID = data["id"]

module = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, module)
from logging_config import logger

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
moduleAsym = os.path.join(module, 'Module', 'Encryption')
modulePath = os.path.join(module, 'Module')
sys.path.insert(0, modulePath)
sys.path.insert(0, moduleAsym)
moduleSym = os.path.join(module, 'Module', 'SysmetricEncryption')
sys.path.insert(0, moduleSym)

module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, os.path.join(module, 'Module', 'SendStrategy'))
sys.path.insert(0, os.path.join(module, 'Module', 'PathStrategy'))
sys.path.insert(0, os.path.join(module, 'Module', 'Email'))

# print("Check all paths in sys path:")
# for path in sys.path:
#     print("\t- ", path)

from Module.MixNode import *
from Module.schemas import EmailRequest, Message
from Module.MixNode import MixNode
from NonProbabilisticPathGenerationStrategy import NonProbabilisticPathGenerationStrategy
from ProbabilisticPathSelectionStrategy import ProbabilisticPathGenerationStrategy
from TimedSendStrategy import TimedSendStrategy
from Email import Email
from EncryptionManager import EncryptionManager
from SysmetricEncryptionManager import SysmetricEncryptionManager

managerAsym = EncryptionManager(os.path.join(moduleAsym, 'Algorithms'))
managerSym = SysmetricEncryptionManager(os.path.join(moduleSym, 'Algorithms'))
algorithm_name = "rsa_encryption"

# public_key = managerAsym.get_public_key(algorithm_name)
# print(public_key)

send_strategy = TimedSendStrategy(10)

gmail = Email()
gmail.get_email_from_json(STORAGE_PATH + "mail_acc.json")

mix_node = MixNode(asymmetric_encrytion_manager=managerAsym, symmetric_encryption_manager=managerSym, send_strategy=send_strategy, email=gmail, path_strategy=ProbabilisticPathGenerationStrategy())


app = FastAPI()
# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Allow GET and POST requests
    allow_headers=["*"],  # Allow all headers
)


# Define the hello page
@app.get("/")
async def read_root():
    logger.info(f"MIX_NODE {ID}: Root endpoint called.")
    return "This is node Server."


@app.get("/receiveMessage")
async def receive_email(request: Request):
    try:
        message = await request.json()
        logger.info(f"MIX_NODE {ID}: Received message: {message}")
        return {"status": "success", "message": "Message received successfully"}
    except Exception as e:
        logger.error(f"MIX_NODE {ID}: Error receiving message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sendEmail")
async def send_email(request: EmailRequest):
    try:
        logger.info(f"MIX_NODE {ID}: Sending email with request: {request}")
        return {"status": "success", "message": "Email sent successfully"}
    except Exception as e:
        logger.error(f"MIX_NODE {ID}: Error sending email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/receiveEmail")
async def receive_email(message: Message):
    try:
        # logger.info(f"MIX_NODE {ID}: Received email: {message.model_dump()}")
        mix_node.receive_and_add_to_queue(message)
        return {"status": "success", "message": "Email received successfully"}
    except Exception as e:
        # logger.error(f"MIX_NODE {ID}: Error receiving email: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    
@app.get("/updateSymmetricAlgorithm")
async def update_symmetric_algorithm(algorithm_name: str):
    try:
        mix_node.update_symmetric_algorithm(algorithm_name)
        logger.info(f"MIX_NODE {ID}: Symmetric algorithm updated to {algorithm_name}.")
        return {"status": "success", "message": "Symmetric algorithm updated successfully"}
    except Exception as e:
        logger.error(f"MIX_NODE {ID}: Error updating symmetric algorithm: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/updateAsymmetricAlgorithm")
async def update_asymmetric_algorithm(algorithm_name: str):
    try:
        mix_node.update_asymmetric_algorithm(algorithm_name)
        logger.info(f"MIX_NODE {ID}: Asymmetric algorithm updated to {algorithm_name}.")
        return {"status": "success", "message": "Asymmetric algorithm updated successfully"}
    except Exception as e:
        logger.error(f"MIX_NODE {ID}: Error updating asymmetric algorithm: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

def get_beginning_info():
    try:
        with open(config_file, 'r') as file:
            data = json.load(file)
        
        id, ip = data["id"], re.sub(r"http://localhost:(\d+)", r"127.0.0.1:\1", data["ip"])
        logger.info(f"MIX_NODE {id}: Starting node.\n\t- id: {id}\t- ip: {ip}")

        # Get the list of available algorithms
        available_algorithms = managerAsym.get_available_algorithms()
        logger.info(f"MIX_NODE {ID}: \tAvailable algorithms:\n\t\tAsymmetric: {available_algorithms}")
        logger.info(f"MIX_NODE {ID}: \t\tSymmetric: {managerSym.get_available_algorithms()}")
    except Exception as e:
        logger.error(f"MIX_NODE {ID}: Error getting initial info: {str(e)}")



if __name__ == '__main__':
    get_beginning_info()
    uvicorn.run(app, host="0.0.0.0", port=8001)  # , ssl_certfile="cert.pem", ssl_keyfile="key.pem")



