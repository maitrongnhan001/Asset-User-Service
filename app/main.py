from fastapi import Depends, FastAPI

from .dependencies import get_token_header
from .internal import admin
from .controllers import users
from .controllers import assets

app = FastAPI()

app.include_router(users.router)
app.include_router(assets.router)
app.include_router(
    admin.router,
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}},
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}