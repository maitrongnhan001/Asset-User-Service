from eth_account import Account
import secrets
from fastapi import APIRouter
from ..models import users
from ..helpers import responseDto
from fastapi import APIRouter, HTTPException
import bcrypt

router = APIRouter()

class UserController:
    email: str
    password: str
    dob: str

@router.post("/users/register", tags=["create user"])
async def CreateUser(userData: UserController):
    # Generate user wallet
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)

    print ("SAVE BUT DO NOT SHARE THIS:", private_key)
    print("Address:", acct.address)

    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(userData.password.encode('utf-8'), salt)

    isUserCreated = users.User(userData.email, hashed_password, userData.dob, acct.address, private_key)

    if (isUserCreated) :
        print("User created")

        return responseDto.ResponseDTO(200, "Register user successfully", {
            "email": userData.email,
            "dob": userData.dob,
            "address": acct.address,
        })
    else:
        print("Failed to created")

        raise HTTPException(status_code=400, detail="Failed to create user")

