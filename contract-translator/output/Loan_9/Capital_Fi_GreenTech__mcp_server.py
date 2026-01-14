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
    Retrieve lender information.

    Returns:
        dict: A dictionary containing lender details.
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """
    Retrieve borrower information.

    Returns:
        dict: A dictionary containing borrower details.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerms(index):
    """
    Retrieve financial terms based on the index.

    Parameters:
        index (int): The index of the financial terms to retrieve.

    Returns:
        dict: A dictionary containing financial terms.
    """
    try:
        result = contract.functions.getFinancialTerms(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getImportantDate(index):
    """
    Retrieve important date based on the index.

    Parameters:
        index (int): The index of the important date to retrieve.

    Returns:
        dict: A dictionary containing important date information.
    """
    try:
        result = contract.functions.getImportantDate(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """
    Retrieve obligation details based on the index.

    Parameters:
        index (int): The index of the obligation to retrieve.

    Returns:
        dict: A dictionary containing obligation details.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(index):
    """
    Fulfill an obligation based on the given index.

    Parameters:
        index (int): The index of the obligation to fulfill.

    Returns:
        dict: A dictionary containing the transaction hash.
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

@mcp.tool()
def checkLoanAmount():
    """
    Check if the loan amount is valid.

    Returns:
        dict: A dictionary indicating whether the loan amount is valid.
    """
    try:
        result = contract.functions.checkLoanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calculateDefaultInterest(unpaidAmount):
    """
    Calculate the default interest based on the unpaid amount.

    Parameters:
        unpaidAmount (int): The unpaid amount for which to calculate interest.

    Returns:
        dict: A dictionary containing the calculated interest.
    """
    try:
        result = contract.functions.calculateDefaultInterest(unpaidAmount).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()