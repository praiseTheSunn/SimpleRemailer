import base64
import json
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

from NodeServer.Module.schemas import EmailRequest, Message, DecryptedData, HeaderInfo

import sys
import os
import requests

# Get the absolute path of the project root directory
module = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))

# Construct the path to the your_project directory
module = os.path.join(module, 'Module', 'Encryption')

# Add your_project directory to the Python path
sys.path.insert(0, module)

# Now you can import EncryptionManager
from EncryptionManager import EncryptionManager

# Assuming algorithm classes are in the 'Algorithms' directory
manager = EncryptionManager(os.path.join(module, 'Algorithms'))

# Get the list of available algorithms
available_algorithms = manager.get_available_algorithms()
print(f"Available algorithms: {available_algorithms}")

algorithm_name = "ecc_encryption"
private_key_pem, public_key_pem = manager.generate_keys(algorithm_name)

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
    return {"message": "Hello, World!"}

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
        decoded_content = message.content.encode('utf-8')
        encryption_algorithm = message.header.encryption_algorithm

        # Decrypt the data
        decrypted_data = manager.decrypt(encryption_algorithm, private_key_pem, decoded_content)

        # Parse the decrypted data into class DecryptedData
        decrypted_data = DecryptedData.parse_raw(decrypted_data)
        next_node_encrypted_data = decrypted_data.next_node_encrypted_data
        next_ip = decrypted_data.next_ip

        if decrypted_data.flag_end:
            print("Email received successfully")
        else:
            requests.post(f"http://{next_ip}:8000/receiveEmail", 
                          json=Message(header=HeaderInfo(encryption_algorithm=encryption_algorithm), 
                                       content=next_node_encrypted_data))

        return {"status": "success", "message": "Email received successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New route to send the first message to the /receiveEmail route
@app.post("/sendFirstMessage")
async def send_first_message(request: EmailRequest):
    try:
        # Encrypt the data
        encryption_algorithm = "ecc_encryption"  # Specify the encryption algorithm
        encrypted_content = manager.encrypt(encryption_algorithm, public_key_pem, request.content)

        # Create a Message object
        message = Message(
            header=HeaderInfo(encryption_algorithm=encryption_algorithm),
            content=base64.b64encode(encrypted_content).decode('utf-8')
        )

        # Send the message to the /receiveEmail route
        response = requests.post("http://localhost:8000/receiveEmail", json=message.dict())
        response.raise_for_status()  # Raise an error if the request was not successful

        return {"status": "success", "message": "First message sent successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    request = EmailRequest(
        email="hoang2003@gmai.com",
        subject="Hello",
        message="Hello, World!"
    )
    # Convert the request to dictionary, then to JSON string, and finally to bytes
    request_dict = request.model_dump()
    request_json = json.dumps(request_dict)
    request_bytes = request_json.encode('utf-8')
    # request_bytes_str = base64.b64encode(request_bytes).decode('utf-8')

    # tmp = request_bytes_str

    # data = DecryptedData(
    #     flag_end=True,
    #     path_strategy="",
    #     flag_starting_node=True,
    #     next_ip="",
    #     next_node_encrypted_data="hoang2003ngolike@gmail.com|Hello|Hello, World!"
    #     # next_node_encrypted_data=request_bytes_str
    # )
    # data_dict = data.model_dump()
    # data_json = json.dumps(data_dict)
    # print("?????", data_json)
    # data_bytes = data_json.encode('utf-8')

    encryption_algorithm = "rsa_encryption"  # Specify the encryption algorithm
    # run main server then paste correct public key
    public_key_pem = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAvB8sa/Cg5N2yN8ze5FCS\nJce0RTIjCpHysGQm7YW5jDQ1j5LTctH8/pOynx1UUypfcmG4jtiHg8dWSZJQKSGe\nzKNHK9H2QrnwpqOwDikfosPtbIbEELxdA86SaoR43NesGwub4Tb+Oa21XGdoIlWn\n3ImTZyVbajtwle1Xck1ivFSH7KrZevX9LR/doRn25bHPcFReiSVmJ+oNGw0Uqcu2\nV4smjDprk2dCW+OiWaenJIRYbptJODk8F9BxDg454dBFzV1eU3q3xfc5d8hNJ9T8\ntQLYFdiK4m3bOD//jBf8ilOWFOgBPUJ+GjL+LoORDBzl4MJG4UHyzOgjIJh0az+w\nOwIDAQAB\n-----END PUBLIC KEY-----\n'
    encrypted_content = manager.encrypt(encryption_algorithm, public_key_pem, request_bytes)

    tmp = base64.b64encode(encrypted_content).decode('utf-8')
    print(tmp)

    # rounds = 2
    # public_keys = [b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEApz/tocVMET8oZ02gaLBe\nARLwbe1FxdFFn0CMjljybntDrMsZkrmCvvGyoUndwbNvmErMEncemzR/QhQfJBLU\nTfvAO2Wt94HgE5MP9goJSiH74XlPrXwN514fB7gbq2oiCOvZxTW8dGo6TjCRNISM\nctsNRxNb8QoVLdBFGtkJVHKqBP0aGEFholmVAfZoIlqofaA/6wJHoXSf6ycQKlqH\nur5jYnjjdl1WMnzrAAyg71F0tzspZz4woQtlidKPs0aaYd0O6sok2I6vQaFO9fRd\ntGms4O5CHQDtUwihQ/sXSgWhFsSxTB62cVvlV4ONqF1GRklYJoZEfXpVQPSY8oqW\nWQIDAQAB\n-----END PUBLIC KEY-----\n', 
    #                b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsY2bFEF2nz7QpVP4RL7o\nKa3THpfXYMvrXF0s30hLdSWSR9E2V8G4HibNXDHNuLBsaa0igBVpgqjAhBVgqyty\nsehiBNjRmMbjvFl99FgnqNYJu3dctD7dlmw8KEcXeLdPGhP0yC1Rkl1B9I/gXCbf\n0AeToX1VGoWRJHKsdcNPmmjGVOTx6M+tk1v+JbWedMp3WDOP5GhyIJvgoxVDGGVx\nk+Ks9oI1ErkLZ6L+mb6TQF1dqDTXvP+t99zDyv0H4xKWT7BzHVs/O7UcwXZdvBBC\nnsfcbriygb5HaDVPnAVT2YDOj8Z1AaUtt3pxMzxNFq36GKRist9vcsjxzT3by126\nUwIDAQAB\n-----END PUBLIC KEY-----\n']
    # ip = ['0.0.0.0:8002', '0.0.0.0:8000']

    # for i in range(rounds):
    #     data = DecryptedData(
    #         flag_end=False if i < rounds - 1 else True,
    #         path_strategy="",
    #         flag_starting_node=False,
    #         next_ip="localhost",
    #         next_node_encrypted_data=tmp
    #     )
    #     data_dict = data.model_dump()
    #     data_json = json.dumps(data_dict)
    #     data_bytes = data_json.encode('utf-8')

    #     encryption_algorithm = "rsa_encryption"  # Specify the encryption algorithm
    #     public_key_pem = public_keys[i]
    #     encrypted_content = manager.encrypt(encryption_algorithm, public_key_pem, data_bytes)

    #     tmp = base64.b64encode(encrypted_content).decode('utf-8')

    # Create a Message object
    message = Message(
        header=HeaderInfo(encryption_algorithm=encryption_algorithm),
        content=tmp
    )


    # Ensure that message.model_dump() is a dictionary with serializable values
    message_dict = message.model_dump()

    # Send the message to the /receiveEmail route
    response = requests.post("http://localhost:8000/receiveEmail", json=message_dict)

    # uvicorn.run(app, host="0.0.0.0", port=8001)#, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
