from web3 import Web3
from web3.middleware import geth_poa_middleware
from decouple import config
import json
import os

BLOCKCHAIN_AVAX_RPC         = config("BLOCKCHAIN_AVAX_RPC")
ASSET_CONTRACT_ADDRESS      = config("ASSET_CONTRACT_ADDRESS")
APPLICATION_URL             = config("APPLICATION_URL")

async def BlockchainConnect():
    try:
        w3 = Web3(Web3.HTTPProvider(BLOCKCHAIN_AVAX_RPC))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        if (not w3.is_connected()) :
            raise Exception()
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return w3

async def AssetConnect():
    try:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(current_directory, '.', 'abis', 'Asset.sol', 'Asset.json')
        AssetABIStr = open(json_file_path, "r")
        AssetABI = json.load(AssetABIStr)
        AssetABIStr.close()

        w3 = await BlockchainConnect()
        print(ASSET_CONTRACT_ADDRESS)
        assetContract = w3.eth.contract(address=ASSET_CONTRACT_ADDRESS, abi=AssetABI["abi"])
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return assetContract

async def CreateAnAsset(caller: str, callerPrivateKey: str, tokenURI: str):
    try:
        w3 = await BlockchainConnect()
        assetContract = await AssetConnect()

        nonce = w3.eth.get_transaction_count(caller)
        chain_id = w3.eth.chain_id
        call_function = assetContract.functions.mint(tokenURI).build_transaction({
            "chainId"   : chain_id,
            "gasPrice"  : w3.eth.gas_price,
            "from"      : caller,
            "nonce"     : nonce
        })
        signed_tx = w3.eth.account.sign_transaction(call_function, private_key=callerPrivateKey)
        send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)
        print("Mint NFT successfully")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return tx_receipt

async def GetNewestAsset(address: str):
    try:
        w3 = await BlockchainConnect()
        assetContract = await AssetConnect()


        
        print("Mint NFT successfully")
    except ZeroDivisionError:
        print("Error: Division by zero is not allowed!")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("This block always executes, regardless of whether an exception occurred or not.")
    return tx_receipt