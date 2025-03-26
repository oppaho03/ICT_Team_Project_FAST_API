import httpx

RASA_SERVER = "http://localhost:5005/webhooks/rest/webhook"

async def ask_rasa(message: str, sender: str = "user") -> str:
    payload = {
        "sender": sender,
        "message": message
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(RASA_SERVER, json=payload)
        response.raise_for_status()
        data = response.json()

    # Rasa는 응답을 list 형식으로 반환함
    return " ".join([msg.get("text", "") for msg in data])
