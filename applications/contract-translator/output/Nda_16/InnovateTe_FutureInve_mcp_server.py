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
    """Retrieve the Disclosing Party's information.

    Returns:
        dict: A dictionary containing information about the Disclosing Party.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Retrieve the Receiving Party's information.

    Returns:
        dict: A dictionary containing information about the Receiving Party.
    """
    try:
        result = contract.functions.getReceivingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Retrieve the start date of the NDA.

    Returns:
        dict: A dictionary containing the start date and a timestamp.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEndDate():
    """Retrieve the end date of the NDA.

    Returns:
        dict: A dictionary containing the end date and a timestamp.
    """
    try:
        result = contract.functions.getEndDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation():
    """Retrieve the obligations defined in the NDA.

    Returns:
        dict: A dictionary containing the obligations.
    """
    try:
        result = contract.functions.getObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConditions():
    """Retrieve the conditions specified in the NDA.

    Returns:
        dict: A dictionary containing the conditions.
    """
    try:
        result = contract.functions.getConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def executeObligation():
    """Execute the obligations defined in the NDA.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.executeObligation().buildTransaction({
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