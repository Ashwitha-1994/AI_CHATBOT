print("APP STARTED")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#from backend.routes.voice import router as voice_router
from backend.routes.chat import router

app = FastAPI(
    title=" AI Chatbot",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

@app.get("/")
def home():
    return {
        "status": "success",
        "message": "Chatbot is running 🚀"
    }