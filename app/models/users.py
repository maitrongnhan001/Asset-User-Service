from prisma import Prisma
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import bcrypt
import jwt

class User:
    email: str
    password: str
    dob: str
    address: str
    private_key: str

    def __init__(self, email, password, dob, address, private_key):
        self.email = email
        self.password = password
        self.dob = dob
        self.address = address
        self.private_key = private_key

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
    skip: int = 0, 
    limit: int = 10,
    field: str = None,
    value: str = None
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
            print(field)
            listUsers = await db.users.find_many(take=limit, skip=skip, where=whereObj)
            total = await db.users.count(where=whereObj)
        else:
            print(field)
            print("debug")
            listUsers = await db.users.find_many(take=limit, skip=skip)
            total = await db.users.count()

        await db.disconnect()

        return {
            "list": listUsers,
            "limit": limit,
            "skip": skip,
            "total": total
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
    email: str,
    password: str
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
        if (bcrypt.checkpw(password.encode("utf-8"), user.password)):
            # Generate the jwt token
            userPayload = {
                "id": user.id,
                "email": user.email,
                "dob": user.dob,
                "address": user.address
            }

            return {
                "accessToken": jwt.encode(userPayload, "secret", algorithm="SHA256"),
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