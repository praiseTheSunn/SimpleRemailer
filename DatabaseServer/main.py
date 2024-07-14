# main.py

import uvicorn
from fastapi import FastAPI
from module.encryption import router as encryption_router

app = FastAPI()


@app.get("/")
def read_root():
    return "This is database server."

# Include the encryption router
app.include_router(encryption_router, prefix="/encryption")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
