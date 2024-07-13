from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from schemas import EmailRequest
from PathDeterminator import PathDeterminator, FullPathStrategy, PartialPathStrategy

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
    uvicorn.run(app, host="0.0.0.0", port=8001, ssl_certfile="cert.pem", ssl_keyfile="key.pem")
