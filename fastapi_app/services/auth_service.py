from fastapi import Header, HTTPException
from jose import JWTError, jwt
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class AuthService:
    def __init__(self):
        self.secret_key = SECRET_KEY
        self.algorithm = ALGORITHM

    async def get_current_user(self, authorization: str = Header(...)) -> str:
        try:
            token = authorization.split(" ")[1]
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            user_id = payload.get("user_id")
            if user_id is None:
                raise HTTPException(status_code=401, detail="Invalid token payload")
            return user_id
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid JWT token")