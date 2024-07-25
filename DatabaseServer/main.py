# main.py

import uvicorn
from fastapi import FastAPI
from module.encryption import router as encryption_router
from module.symmetric_encryption import router as symmetric_encryption_router
from module.node import router as node
app = FastAPI()


@app.get("/")
def read_root():
    return "This is database server."

# Include the encryption router
app.include_router(encryption_router, prefix="/encryption")
app.include_router(symmetric_encryption_router, prefix="/symmetric_encryption")
app.include_router(node, prefix="/node")

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
