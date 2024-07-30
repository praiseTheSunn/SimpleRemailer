from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import sys
import os

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

mix_node = MixNode(asymmetric_encrytion_manager=managerAsym, symmetric_encryption_manager=managerSym, send_strategy=send_strategy, email=gmail, path_strategy=NonProbabilisticPathGenerationStrategy())


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
    return "This is node Server."


@app.get("/receiveMessage")
async def receive_email(request: Request):
    try:
        message = await request.json()
        print(message)
        return {"status": "success", "message": "Email received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sendEmail")
async def send_email(request: EmailRequest):
    try:
        return {"status": "success", "message": "Email sent successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/receiveEmail")
async def receive_email(message: Message):
    try:
        print("\nNEW MESSAGE: \n", message)
        print()
        mix_node.receive_and_add_to_queue(message)

        return {"status": "success", "message": "Email received successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/updateSymmetricAlgorithm")
async def update_symmetric_algorithm(algorithm_name: str):
    try:
        mix_node.update_symmetric_algorithm(algorithm_name)
        return {"status": "success", "message": "Symmetric algorithm updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/updateAsymmetricAlgorithm")
async def update_asymmetric_algorithm(algorithm_name: str):
    try:
        mix_node.update_asymmetric_algorithm(algorithm_name)
        return {"status": "success", "message": "Asymmetric algorithm updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# class StrategyRequest(BaseModel):
#     strategy: str
#     i: int = 1

# @app.post("/set_strategy")
# async def set_strategy(request: StrategyRequest):
#     if request.strategy == 'full':
#         pathDeterminator.set_strategy(FullPathStrategy())
#     elif request.strategy == 'partial':
#         pathDeterminator.set_strategy(PartialPathStrategy(request.i))
#     else:
#         raise HTTPException(status_code=400, detail="Unknown strategy")
#     return {"message": "Strategy updated"}

# @app.post("/sendEmail")
# async def send_email(request: EmailRequest):
#     try:
#         email_sent = True  # Mocking the email sending logic
#         path = pathDeterminator.determine_path()
#         print(request, path)

#         if email_sent:
#             return {"status": "success", "message": "Email sent successfully"}
#         else:
#             raise HTTPException(status_code=500, detail="Failed to send email")

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


def get_beginning_info():
    with open(STORAGE_PATH + "config.json", 'r') as file:
        data = json.load(file)

    id, ip = data["id"], re.sub(r"http://localhost:(\d+)", r"127.0.0.1:\1", data["ip"])
    print(f"THIS IS A MIX NODE\n\t- id: {id}\t- ip: {ip}")

    # Get the list of available algorithms
    available_algorithms = managerAsym.get_available_algorithms()
    print(f"\tAvailable algorithms:\n\t\tAsymmetric:{available_algorithms}")
    print(f"\t\tSysmetric:{managerSym.get_available_algorithms()}")

if __name__ == '__main__':
    get_beginning_info()
    uvicorn.run(app, host="0.0.0.0", port=8001)  # , ssl_certfile="cert.pem", ssl_keyfile="key.pem")



