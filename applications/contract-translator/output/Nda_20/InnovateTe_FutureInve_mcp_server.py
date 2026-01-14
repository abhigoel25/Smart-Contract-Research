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
    """Retrieve the details of the disclosing party.
    
    Returns:
        dict: Contains name, role, and addressLine of the disclosing party.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"name": result[0], "role": result[1], "addressLine": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Retrieve the details of the receiving party.
    
    Returns:
        dict: Contains name, role, and addressLine of the receiving party.
    """
    try:
        result = contract.functions.getReceivingParty().call()
        return {"name": result[0], "role": result[1], "addressLine": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Retrieve the start date of the agreement.
    
    Returns:
        dict: Contains dateType, value, and dayOfMonth.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"dateType": result[0], "value": result[1], "dayOfMonth": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConfidentialityEndDate():
    """Retrieve the confidentiality end date of the agreement.
    
    Returns:
        dict: Contains dateType, value, and dayOfMonth.
    """
    try:
        result = contract.functions.getConfidentialityEndDate().call()
        return {"dateType": result[0], "value": result[1], "dayOfMonth": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligationCount():
    """Retrieve the count of obligations in the agreement.
    
    Returns:
        dict: Contains the count of obligations.
    """
    try:
        result = contract.functions.getObligationCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index: int):
    """Retrieve the details of a specific obligation by index.
    
    Args:
        index (int): The index of the obligation.
    
    Returns:
        dict: Contains the party, description, deadline, and penaltyForBreach.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {
            "party": result[0],
            "description": result[1],
            "deadline": result[2],
            "penaltyForBreach": result[3],
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()