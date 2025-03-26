from fastapi import APIRouter
from pydantic import BaseModel
from services.rasa_service import ask_rasa

router = APIRouter()

class Message(BaseModel):
    message: str
    sender: str = "user"

@router.post("/chat")
async def chat_with_rasa(payload: Message):
    reply = await ask_rasa(payload.message, payload.sender)
    return {"response": reply}
