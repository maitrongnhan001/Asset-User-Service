from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..auth import auth_bearer
from ..helpers import jwtHelper
from ..models import asset
from ..helpers import responseDto

router = APIRouter()

class AssetCreateController(BaseModel):
    picture         : str
    price           : float
    metadata        : str
    certificate     : str

@router.post("/api/assets/create", tags=["Create assets"])
async def CreateAsset(
    assetInput: AssetCreateController,
    token: str = Depends(auth_bearer.JWTBearer())
):
    payload = jwtHelper.decodeJWT(token)
    assertCreated = await asset.CreateAnAsset(payload.id, assetInput.picture, assetInput.price, assetInput.metadata, assetInput.certificate)
    return responseDto.ResponseDTO(200, "Create an asset successfully", assertCreated)