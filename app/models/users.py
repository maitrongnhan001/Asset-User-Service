from prisma import Prisma
from eth_account import Account
import secrets

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

        db.users.create(user)

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
    