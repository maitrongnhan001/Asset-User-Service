from eth_account import Account
import secrets
from fastapi import APIRouter
from ..models import users
from ..helpers import responseDto
from fastapi import APIRouter, HTTPException
import bcrypt
from pydantic import BaseModel

router = APIRouter()

class UserController(BaseModel):
    email: str
    password: str
    dob: str

class UserLoginController(BaseModel):
    email: str
    password: str

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

    userWillCreate = users.User(userData.email, hashed_password, userData.dob, acct.address, private_key)
    isUserCreated = await users.CreateUser(userWillCreate)

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

@router.get("/users/", tags=["List users"])
async def ListUsers(
    skip: int = 0, 
    limit: int = 10,
    field: str = None,
    value: str = None
):
    listUsers = await users.ListUsers(skip, limit, field, value)
    
    if (len(listUsers) > 0):
        return responseDto.ResponseDTO(200, "Get the list users successfully", listUsers)
    else:
        return responseDto.ResponseDTO(404, "The user not found", listUsers)
    
@router.post("/users/login", tags=["Login"])
async def Login(userLoginController: UserLoginController):
    userLogin = await users.Login(userLoginController.email, userLoginController.password)
    return responseDto.ResponseDTO(200, "Login successfully", userLogin)
