from eth_account import Account
import secrets
from fastapi import APIRouter
from ..models import users
from ..helpers import responseDto
from fastapi import APIRouter, HTTPException, Depends
import bcrypt
from pydantic import BaseModel
from ..auth import auth_bearer
from ..helpers import jwtHelper

router = APIRouter()

class UserController(BaseModel):
    email       : str
    password    : str
    dob         : str

class UserLoginController(BaseModel):
    email       : str
    password    : str

class UserUpdateController(BaseModel): 
    password    : str = None
    avatar      : str = None
    dob         : str = None
    country     : str = None
    city        : str = None

@router.post("/users/register", tags=["Create user"])
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


@router.get("/users/me", tags=["Get my information"])
async def GetMe(token: str = Depends(auth_bearer.JWTBearer())):
    payload = jwtHelper.decodeJWT(token)

    user = await users.GetMe(payload.id)

    return responseDto.ResponseDTO(200, "Get user information successfully", user)

@router.put("/users/update", tags=["Update user"])
async def UpdateUser(userUpdateController: UserUpdateController, token: str = Depends(auth_bearer.JWTBearer())):
    payload = jwtHelper.decodeJWT(token)
    userUpdated = await users.UpdateUser(
        payload.id,
        userUpdateController.password,
        userUpdateController.avatar,
        userUpdateController.dob,
        userUpdateController.country,
        userUpdateController.city,
    )
    return responseDto.ResponseDTO(200, "Update user successfully", userUpdated)