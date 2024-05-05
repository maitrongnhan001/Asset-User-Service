from ..services import Asset
from prisma import Prisma
from fastapi.encoders import jsonable_encoder
from decouple import config
from fastapi import HTTPException

APPLICATION_URL = config("APPLICATION_URL")

class AssetData:
    isMine      : bool
    picture     : str
    price       : str
    metadata    : str
    certificate : str
    owner_id    : str

    def __init__(self, isMine, picture, price, metadata, certificate, owner_id):
        self.isMine         = isMine
        self.picture        = picture
        self.price          = price
        self.metadata       = metadata
        self.certificate    = certificate
        self.owner_id       = owner_id

async def CreateAnAsset(
    userId      : str,
    picture     : str,
    price       : float,
    metadata    : str,
    certificate : str
):
    try:
        # Store data to database
        db = Prisma()

        await db.connect()

        assetWillCreate = AssetData(False, picture, price, metadata, certificate, userId)

        assertCreated = await db.assets.create(jsonable_encoder(assetWillCreate))

        user = await db.users.find_unique(where={"id": userId})

        # Take an interaction with Asset smart contract to receive the Asset data
        tokenUrl = APPLICATION_URL + "/api/asset/" + assertCreated.id
        trxData = await Asset.CreateAnAsset(user.address, user.private_key, tokenUrl)
        tokenId = int.from_bytes(trxData["logs"][0]["topics"][3], byteorder='big')

        # Update token id
        await db.assets.update(data={"isMine": True, "tokenId": str(tokenId)}, where={"id": assertCreated.id})

        asset = await db.assets.find_unique(where={"id": assertCreated.id})

        await db.disconnect()
        result = asset
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to create asset")
        result = False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to create asset")
        result = False
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return result

async def ListAssets(
    skip    : int = 0, 
    limit   : int = 10,
    field   : str = None,
    value   : str = None
):
    try:
        db = Prisma()
        await db.connect()
        listAssets = []
        total = 0
        if (field):
            whereObj = {
                field: value
            }
            listAssets = await db.assets.find_many(
                take=limit, 
                skip=skip, 
                where=whereObj
            )
            total = await db.assets.count(where=whereObj)
        else:
            listAssets = await db.assets.find_many(
                take=limit, 
                skip=skip
            )
            total = await db.users.count()

        await db.disconnect()

        return {
            "list"      : listAssets,
            "limit"     : limit,
            "skip"      : skip,
            "total"     : total
        }
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to list asset")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to list asset")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")

async def GetAsset(
    id: str
):
    try:
        db = Prisma()
        await db.connect()
        
        asset = await db.assets.find_unique(where={"id": id})

        await db.disconnect()

        return asset
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to get asset")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to get asset")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")