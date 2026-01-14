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
    """Fetches the lender information.

    Returns:
        dict: Lender name, address, and additional information.
    """
    try:
        result = contract.functions.getLender().call()
        return {"lender_name": result[0], "lender_address": result[1], "additional_info": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Fetches the borrower information.

    Returns:
        dict: Borrower name, address, and additional information.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"borrower_name": result[0], "borrower_address": result[1], "additional_info": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index):
    """Fetches the financial terms for a given index.

    Args:
        index (int): The index of the financial term.

    Returns:
        dict: Financial term details.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "term_number": result[0],
            "term_type": result[1],
            "term_description": result[2],
            "term_value": result[3],
            "additional_info": result[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDateDetail(index):
    """Fetches date details for a given index.

    Args:
        index (int): The index of the date detail.

    Returns:
        dict: Date detail information.
    """
    try:
        result = contract.functions.getDateDetail(index).call()
        return {
            "date_description": result[0],
            "date_type": result[1],
            "date_value": result[2]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def executeObligation(index):
    """Executes an obligation defined by index.

    Args:
        index (int): The index of the obligation to execute.

    Returns:
        dict: Transaction hash of the executed obligation.
    """
    try:
        txn = contract.functions.executeObligation(index).buildTransaction({
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
def makePayment(amount):
    """Makes a payment to the contract.

    Args:
        amount (int): The amount to pay in wei.

    Returns:
        dict: Transaction hash of the payment made.
    """
    try:
        txn = contract.functions.makePayment(amount).buildTransaction({
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