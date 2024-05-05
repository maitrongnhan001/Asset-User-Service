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

@router.post("/api/assets/create", tags=["Assets"])
async def CreateAsset(
    assetInput: AssetCreateController,
    token: str = Depends(auth_bearer.JWTBearer())
):
    payload = jwtHelper.decodeJWT(token)
    assertCreated = await asset.CreateAnAsset(payload.id, assetInput.picture, assetInput.price, assetInput.metadata, assetInput.certificate)

    if (not assertCreated):
        return responseDto.ResponseDTO(500, "There are errors", {})

    return responseDto.ResponseDTO(200, "Create an asset successfully", assertCreated)

@router.get("/api/assets/", tags=["Assets"])
async def ListAssets(
    skip    : int = 0, 
    limit   : int = 10,
    field   : str = None,
    value   : str = None
):
    listAsset = await asset.ListAssets(skip, limit, field, value)
    
    if (len(listAsset) > 0):
        return responseDto.ResponseDTO(200, "Get the list asset successfully", listAsset)
    else:
        return responseDto.ResponseDTO(404, "The user not found", listAsset)
    
@router.get("/api/assets/{id}", tags=["Assets"])
async def GetAsset(id: str):
    return await asset.GetAsset(id)