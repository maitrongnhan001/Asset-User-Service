import time
import jwt
from decouple import config

JWT_SECRET      = config("JWT_SECRET_KEY")
JWT_ALGORITHM   = config("JWT_ALGORITHM")

class UserPayload:
    id          : int
    email       : str
    dob         : str
    address     : str

    def __init__(self, id: int, email: str, dob: str, address: str):
        self.id         = id
        self.email      = email
        self.dob        = dob
        self.address    = address

def decodeJWT(token: str) -> UserPayload | None:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        print(decoded_token["expires"])
        payload = UserPayload(
            decoded_token.get("id"),
            decoded_token.get("email"),
            decoded_token.get("dob"),
            decoded_token.get("address"),
        )

        return payload if decoded_token["expires"] >= time.time() else None
    except:
        return {}