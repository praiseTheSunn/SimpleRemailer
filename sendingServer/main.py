from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from requests import request

from schemas import EmailRequest

from PathDeterminator import PathDeterminator, FullPathStrategy, PartialPathStrategy

app = FastAPI()

pathDeterminator = PathDeterminator(FullPathStrategy())

# Configure CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],  # Only allow GET requests
    allow_headers=["*"],  # Allow all headers
)

@app.route('/set_strategy', methods=['POST'])
def set_strategy():
    strategy_type = request.json.get('strategy')
    if strategy_type == 'full':
        pathDeterminator.set_strategy(FullPathStrategy())
    elif strategy_type == 'partial':
        i = request.json.get('i', 1)
        pathDeterminator.set_strategy(PartialPathStrategy(i))
    else:
        return "Unknown strategy", 400
    return "Strategy updated", 200

@app.post("/sendEmail")
async def send_email(request: EmailRequest):
    try:
        email_sent = True  
        path = pathDeterminator.determine_path()
        print(request, path)

        if email_sent:
            return {"status": "success", "message": "Email sent successfully"}
        else:
            raise HTTPException(status_code=500, detail="Failed to send email")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))           

