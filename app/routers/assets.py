from fastapi import APIRouter

router = APIRouter()


@router.get("/assets/", tags=["assets"])
async def read_users():
    return [{"username": "Rick"}, {"username": "Morty"}]


@router.get("/assets/me", tags=["assets"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/assets/{username}", tags=["assets"])
async def read_user(username: str):
    return {"username": username}