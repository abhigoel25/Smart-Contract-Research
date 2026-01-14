import os
import json
from pathlib import Path
from dotenv import load_dotenv
from web3 import Web3
from fastmcp import FastMCP

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load ABI from the same directory as this script
abi_path = Path(__file__).parent / 'InnovateTe_FutureInve.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("InnovateTe_FutureInve")

@mcp.tool()
def getDisclosingParty():
    """Retrieve the disclosing party's details.

    Returns:
        dict: A dictionary containing name, role, address, and email of the disclosing party.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {
            "name": result[0],
            "role": result[1],
            "addr": result[2],
            "email": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Retrieve the receiving party's details.

    Returns:
        dict: A dictionary containing name, role, address, and email of the receiving party.
    """
    try:
        result = contract.functions.getReceivingParty().call()
        return {
            "name": result[0],
            "role": result[1],
            "addr": result[2],
            "email": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Retrieve the start date of the agreement.

    Returns:
        dict: A dictionary containing date type, value, and day of month.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {
            "dateType": result[0],
            "value": result[1],
            "dayOfMonth": result[2]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEndDate():
    """Retrieve the end date of the agreement.

    Returns:
        dict: A dictionary containing date type, value, and day of month.
    """
    try:
        result = contract.functions.getEndDate().call()
        return {
            "dateType": result[0],
            "value": result[1],
            "dayOfMonth": result[2]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation():
    """Fulfill the obligation under the NDA agreement.

    Returns:
        dict: A dictionary containing the transaction hash of the fulfilled obligation.
    """
    try:
        txn = contract.functions.fulfillObligation().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()