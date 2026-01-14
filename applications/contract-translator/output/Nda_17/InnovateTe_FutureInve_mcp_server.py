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
    """Retrieve information about the disclosing party.
    
    Returns:
        dict: Disclosing party information including name, role, address line, email, and entity type.
    
    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Retrieve information about the receiving party.

    Returns:
        dict: Receiving party information including name, role, address line, email, and entity type.

    Example usage:
        - No parameters required.
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
        dict: Start date information including date type, value, day of month, and frequency.

    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """Retrieve all obligations included in the NDA.

    Returns:
        dict: List of obligations including party, description, deadline, and penalty for breach.

    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """Retrieve any special terms included in the NDA.

    Returns:
        dict: List of special terms as strings.

    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConditions():
    """Retrieve the conditions of the NDA.

    Returns:
        dict: Conditions including exceptions as strings.

    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """Retrieve termination conditions outlined in the NDA.

    Returns:
        dict: List of conditions for termination as strings.

    Example usage:
        - No parameters required.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(obligationIndex):
    """Fulfill a specified obligation in the NDA.

    Args:
        obligationIndex (int): The index of the obligation to fulfill.

    Returns:
        dict: Transaction hash if successful, or error message.

    Example usage:
        - Call with the index of the obligation you want to fulfill.
    """
    try:
        txn = contract.functions.fulfillObligation(obligationIndex).buildTransaction({
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