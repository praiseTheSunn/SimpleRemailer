from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from NodeServer.Module.schemas import EmailRequest, Message
from NodeServer.Module.MixNode import *
from NodeServer.Module.SendStrategy import TimedSendStrategy

import sys
import os

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

# Construct the path to the your_project directory
module = os.path.join(module, 'Module', 'Encryption')

# Add your_project directory to the Python path
sys.path.insert(0, module)

# Now you can import EncryptionManager
from NodeServer.Module.Encryption.EncryptionManager import EncryptionManager

# Assuming algorithm classes are in the 'Algorithms' directory
manager = EncryptionManager(os.path.join(module, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = manager.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")

algorithm_name = "rsa_encryption"
private_key_pem, public_key_pem = manager.generate_keys(algorithm_name)
print(public_key_pem)

send_strategy = TimedSendStrategy.TimedSendStrategy(60)
mix_node = MixNode(manager, send_strategy)

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
        print(message.content)
        mix_node.receive_and_add_to_queue(message)

        return {"status": "success", "message": "Email received successfully"}
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
    uvicorn.run(app, host="0.0.0.0", port=8000)  # , ssl_certfile="cert.pem", ssl_keyfile="key.pem")

