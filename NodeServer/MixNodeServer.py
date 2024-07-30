from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from NodeServer.Module.schemas import EmailRequest, Message
from NodeServer.Module.MixNode import *

from Module.schemas import EmailRequest, Message
from Module.MixNode import MixNode
# from Module.SendStrategy import TimedSendStrategy

import sys
import os

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

# Construct the path to the Module/Encryption directory
moduleAsym = os.path.join(module, 'Module', 'Encryption')

# Construct the path to the Module/Encryption directory
modulePath = os.path.join(module, 'Module')
sys.path.insert(0, modulePath)

# Add the Module/Encryption directory to the Python path
sys.path.insert(0, moduleAsym)

# Construct the path to the your_project directory
moduleSym = os.path.join(module, 'Module', 'SysmetricEncryption')

# Add your_project directory to the Python path
sys.path.insert(0, moduleSym)

module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, os.path.join(module, 'Module', 'SendStrategy'))
sys.path.insert(0, os.path.join(module, 'Module', 'PathStrategy'))
sys.path.insert(0, os.path.join(module, 'Module', 'Email'))
from NodeServer.Module.PathStrategy.CentralizedPathGenerationStrategy import CentralizedPathGenerationStrategy
from NodeServer.Module.SendStrategy.TimedSendStrategy import TimedSendStrategy
from NodeServer.Module.Email.Email import Email

# module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
# sys.path.insert(0, os.path.join(module, 'Module', 'SendStrategy'))
# sys.path.insert(0, os.path.join(module, 'Module', 'PathStrategy'))
# from NodeServer.Module.PathStrategy.CentralizedPathGenerationStrategy import *

# Now you can import EncryptionManager
# from NodeServer.Module.Encryption.EncryptionManager import EncryptionManager
# from NodeServer.Module.SysmetricEncryption.SysmetricEncryptionManager import SysmetricEncryptionManager

# Now you can import EncryptionManager
from EncryptionManager import EncryptionManager
# Now you can import EncryptionManager
from SysmetricEncryptionManager import SysmetricEncryptionManager


# Assuming algorithm classes are in the 'Algorithms' directory
managerAsym = EncryptionManager(os.path.join(moduleAsym, 'Algorithms'))
# Assuming algorithm classes are in the 'Algorithms' directory
managerSym = SysmetricEncryptionManager(os.path.join(moduleSym, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = managerAsym.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")

algorithm_name = "rsa_encryption"

public_key = managerAsym.get_public_key(algorithm_name)
print(public_key)

send_strategy = TimedSendStrategy(10)

gmail = Email()
gmail.get_email_from_json("Storage/mail_acc.json")

mix_node = MixNode(managerAsym, managerSym, send_strategy, gmail)

app = FastAPI()

# pathDeterminator = PathDeterminator(FullPathStrategy())

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

@app.get("/updateSendStrategy")
async def update_send_strategy(strategy_name: str):
    try:
        if (strategy_name == "timed"):
            mix_node.update_send_strategy(TimedSendStrategy(10))
        return {"status": "success", "message": "Send strategy updated successfully"}
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

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8001)  # , ssl_certfile="cert.pem", ssl_keyfile="key.pem")

    # m = Message(encryption_algorithm="rsa_encryption", encrypted_content="encrypted_content", encrypted_key="encrypted_key")
    # mix_node.receive_and_add_to_queue(m)



