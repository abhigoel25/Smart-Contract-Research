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
abi_path = Path(__file__).parent / 'Capital_Fi_GreenTech_.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("Capital_Fi_GreenTech_")

@mcp.tool()
def getLender():
    """
    Retrieves the lender's name and address.
    
    Returns:
        dict: Contains lender's name and address.
    """
    try:
        result = contract.functions.getLender().call()
        return {"name": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """
    Retrieves the borrower's name and address.
    
    Returns:
        dict: Contains borrower's name and address.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"name": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTermsCount():
    """
    Gets the count of financial terms in the loan agreement.
    
    Returns:
        dict: Contains the count of financial terms.
    """
    try:
        result = contract.functions.getFinancialTermsCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index):
    """
    Retrieves a specific financial term by index.
    
    Params:
        index (uint256): The index of the financial term to retrieve.
    
    Returns:
        dict: Contains details about the financial term.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "term_id": result[0],
            "description": result[1],
            "value": result[2],
            "due_date": result[3],
            "other_details": result[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDatesCount():
    """
    Gets the count of important dates in the loan agreement.
    
    Returns:
        dict: Contains the count of important dates.
    """
    try:
        result = contract.functions.getDatesCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDateTerm(index):
    """
    Retrieves a specific date term by index.
    
    Params:
        index (uint256): The index of the date term to retrieve.
    
    Returns:
        dict: Contains details about the date term.
    """
    try:
        result = contract.functions.getDateTerm(index).call()
        return {
            "event": result[0],
            "description": result[1],
            "date": result[2],
            "other_details": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligationsCount():
    """
    Gets the count of obligations in the loan agreement.
    
    Returns:
        dict: Contains the count of obligations.
    """
    try:
        result = contract.functions.getObligationsCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """
    Retrieves a specific obligation by index.
    
    Params:
        index (uint256): The index of the obligation to retrieve.

    Returns:
        dict: Contains details about the obligation.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {
            "description": result[0],
            "details": result[1],
            "penalty": result[2],
            "other_notes": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def processPayment(amount):
    """
    Processes a payment towards the loan.
    
    Params:
        amount (uint256): The amount to be paid.

    Returns:
        dict: Contains transaction hash of the payment.
    """
    try:
        txn = contract.functions.processPayment(amount).buildTransaction({
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