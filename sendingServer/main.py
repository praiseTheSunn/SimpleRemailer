from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import EmailRequest

app = FastAPI()

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow GET requests
    allow_headers=["*"],  # Allow all headers
)

@app.post("/sendEmail")
async def send_email(request: EmailRequest):
    try:
        # Here you would implement the logic to actually send the email.
        # For example, using an email sending service like SMTP or a third-party API.
        # For now, let's just simulate the process.
        email_sent = True  # Simulate email sending process
        print(request)

        if email_sent:
            return {"status": "success", "message": "Email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))           

