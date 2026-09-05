from fastapi import FastAPI
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth_router, user_router, conversation_router
from app.websocket.route import router as websocket_router

Base.metadata.create_all(engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(conversation_router)
app.include_router(websocket_router)


@app.get("/")
def root():
    return {"message": "Welcome to Banter"}
