from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Conversation, ConversationMember, Message
from fastapi.middleware.cors import CORSMiddleware
from app.api.route import router as auth_router

Base.metadata.create_all(engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origins=["*"],
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Welcome to Banter"}
