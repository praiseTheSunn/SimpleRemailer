import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from MixNode import *
from cryptography.hazmat.primitives.asymmetric import rsa



class EncryptedMessage(BaseModel):
    encrypted_message: str

app = FastAPI()

# generate key & gui public key toi server?
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Initialize MixNode with dummy strategies
send_strategy = None
decryption_strategy = None
mix_node = MixNode(private_key, send_strategy, decryption_strategy)

@app.post("/forward/")
async def receive_message(message: EncryptedMessage):
    try:
        mix_node.receive(message.encrypted_message)
        return {"message": "Message received and processed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
