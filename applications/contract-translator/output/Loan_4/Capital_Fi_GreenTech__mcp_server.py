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
    """Get lender information.

    Returns:
        dict: containing lender's information.
    """
    try:
        result = contract.functions.getLender().call()
        return {
            "name": result[0],
            "address": result[2],
            "details": result[1:3] + result[3:]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Get borrower information.

    Returns:
        dict: containing borrower's information.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {
            "name": result[0],
            "address": result[2],
            "details": result[1:3] + result[3:]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index):
    """Get a financial term based on the provided index.

    Args:
        index (int): Index of the financial term.

    Returns:
        dict: containing details about the financial term.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "term": result[0],
            "details": result[1:5]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getImportantDate(index):
    """Get an important date based on the provided index.

    Args:
        index (int): Index of the important date.

    Returns:
        dict: containing details about the important date.
    """
    try:
        result = contract.functions.getImportantDate(index).call()
        return {
            "date": result[0],
            "details": result[1:3] + [result[2]],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """Get an obligation based on the provided index.

    Args:
        index (int): Index of the obligation.

    Returns:
        dict: containing details about the obligation.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {
            "details": result
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makePayment(amount, purpose):
    """Make a payment to the contract.

    Args:
        amount (int): Amount to be paid in wei.
        purpose (str): Reason for making the payment.

    Returns:
        dict: Transaction hash.
    """
    try:
        txn = contract.functions.makePayment(amount, purpose).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(amount, 'ether')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(obligationIndex):
    """Fulfill an obligation based on the provided index.

    Args:
        obligationIndex (int): Index of the obligation to fulfill.

    Returns:
        dict: Transaction hash.
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