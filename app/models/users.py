import time
import json
from prisma import Prisma
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import bcrypt
import jwt
from decouple import config

JWT_SECRET      = config("JWT_SECRET_KEY")
JWT_ALGORITHM   = config("JWT_ALGORITHM")

class User:
    email           : str
    password        : str
    dob             : str
    address         : str
    private_key     : str

    def __init__(self, email, password, dob, address, private_key):
        self.email          = email
        self.password       = password
        self.dob            = dob
        self.address        = address
        self.private_key    = private_key

async def CreateUser (user: User):
    try:
        db = Prisma()
        await db.connect()

        await db.users.create(jsonable_encoder(user))

        await db.disconnect()

        result = True
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        result = False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        result = False
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return result
    
async def ListUsers(
    skip    : int = 0, 
    limit   : int = 10,
    field   : str = None,
    value   : str = None
): 
    try:
        db = Prisma()
        await db.connect()
        listUsers = []
        total = 0
        if (field):
            whereObj = {
                field: value
            }
            listUsers = await db.users.find_many(
                take=limit, 
                skip=skip, 
                where=whereObj
            )
            total = await db.users.count(where=whereObj)
        else:
            listUsers = await db.users.find_many(
                take=limit, 
                skip=skip
            )
            total = await db.users.count()

        await db.disconnect()

        def UserView(user): 
            return {key: value for key, value in user if key != "password"}

        return {
            "list"      : list(map(UserView, listUsers)),
            "limit"     : limit,
            "skip"      : skip,
            "total"     : total
        }
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to list users")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")

async def Login(
    email       : str,
    password    : str
): 
    try:
        db = Prisma()
        await db.connect()
        
        # Get the user information
        user = await db.users.find_unique(where={
            "email": email
        })

        await db.disconnect()

        # Compare the password
        if (bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8"))):
            # Generate the jwt token
            userPayload = {
                "expires"   : time.time() + 86400000,
                "id"        : user.id,
                "email"     : user.email,
                "dob"       : user.dob,
                "address"   : user.address
            }

            return {
                "accessToken": jwt.encode(userPayload, JWT_SECRET, algorithm=JWT_ALGORITHM),
                "user": userPayload
            }
        else:
            raise HTTPException(status_code=401, detail="Un-Authorization")
        
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to list users")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")

async def GetMe(userId: str):
    try:
        db = Prisma()
        await db.connect()

        # Get the user information
        user = await db.users.find_unique(where={
            "id": userId
        })

        await db.disconnect()

        # Return the result to client
        return {
            "id": user.id,
            "email": user.email,
            "avatar": user.avatar,
            "address": user.address,
            "dob": user.dob,
            "country": user.country,
            "city": user.city
        }
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to list users")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")

async def UpdateUser(
    userId      : int,
    password    : str = None,
    avatar      : str = None,
    dob         : str = None,
    country     : str = None,
    city        : str = None
): 
    try:
        db = Prisma()
        await db.connect()
        
        # Check user's update information
        updateObj = json.loads('{}')

        if (password):
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            updateObj["password"] = hashed_password
        
        if (avatar):
            updateObj["avatar"] = avatar
        
        if (dob):
            updateObj["dob"] = dob
        
        if (country):
            updateObj["country"] = country

        if (city):
            updateObj["city"] = city

        # Update to the database
        userUpdated = await db.users.update(updateObj, where={
            "id": userId
        })

        await db.disconnect()

        # Return the result to client
        return userUpdated
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
        raise HTTPException(status_code=500, detail="Failed to list users")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="Failed to list users")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")