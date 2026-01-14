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
abi_path = Path(__file__).parent / 'BlockChain_Venture_Ca.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def getParty(index: int):
    """
    Retrieve the party details based on the index.

    Parameters:
    - index (uint8): The index of the party.

    Returns:
    - dict: A dictionary containing party name, address, and role.
    """
    try:
        result = contract.functions.getParty(index).call()
        return {"party_name": result[0], "address": result[1], "role": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index: int):
    """
    Retrieve the financial term details based on the index.

    Parameters:
    - index (uint8): The index of the financial term.

    Returns:
    - dict: A dictionary containing financial term details.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "amount": result[0],
            "currency": result[1],
            "description": result[2],
            "duration": result[3],
            "interest_rate": result[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index: int):
    """
    Retrieve the obligation details based on the index.

    Parameters:
    - index (uint8): The index of the obligation.

    Returns:
    - dict: A dictionary containing obligation details.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {
            "title": result[0],
            "description": result[1],
            "amount": result[2],
            "status": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(index: int):
    """
    Fulfill the obligation based on the index.

    Parameters:
    - index (uint8): The index of the obligation to fulfill.

    Returns:
    - dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.fulfillObligation(index).buildTransaction({
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