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
    """Retrieve the details of the Disclosing Party.
    
    Returns:
        dict: A dictionary containing details of the Disclosing Party.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Retrieve the details of the Receiving Party.
    
    Returns:
        dict: A dictionary containing details of the Receiving Party.
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
        dict: A dictionary containing the start date as a uint256.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """Retrieve the obligations outlined in the NDA.
    
    Returns:
        dict: A dictionary containing a list of obligations.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """Retrieve the special terms of the NDA.
    
    Returns:
        dict: A dictionary containing special terms as a list of strings.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getExceptionConditions():
    """Retrieve the exception conditions of the NDA.
    
    Returns:
        dict: A dictionary containing the exception conditions as a string.
    """
    try:
        result = contract.functions.getExceptionConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """Retrieve the termination conditions of the NDA.
    
    Returns:
        dict: A dictionary containing termination conditions as a list of strings.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def addObligation(description: str, party: str):
    """Add an obligation to the NDA.
    
    Parameters:
        description (str): The description of the obligation.
        party (str): The party responsible for the obligation.
    
    Returns:
        dict: A dictionary containing the transaction hash of the operation.
    """
    try:
        txn = contract.functions.addObligation(description, party).buildTransaction({
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