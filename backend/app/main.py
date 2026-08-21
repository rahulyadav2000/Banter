from fastapi import FastAPI
from app.database import engine, Base
from app.models import User, Conversation, ConversationMember, Message

Base.metadata.create_all(engine)
app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to Banter"}
