import os
import json
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
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
    """Retrieve the lender's name and address.
    
    Returns:
        dict: A dictionary containing the lender's name and address.
    """
    try:
        result = contract.functions.getLender().call()
        return {"name": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Retrieve the borrower's name and address.
    
    Returns:
        dict: A dictionary containing the borrower's name and address.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"name": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index):
    """Retrieve financial term details by index.
    
    Args:
        index (int): The index of the financial term.
    
    Returns:
        dict: A dictionary containing the financial term details.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "amount": result[0],
            "currency": result[1],
            "purpose": result[2],
            "frequency": result[3],
            "due_date": result[4],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDate(index):
    """Retrieve date details by index.
    
    Args:
        index (int): The index of the date.
    
    Returns:
        dict: A dictionary containing the date details.
    """
    try:
        result = contract.functions.getDate(index).call()
        return {
            "date_type": result[0],
            "value": result[1],
            "day_of_month": result[2],
            "frequency": result[3],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """Retrieve obligation details by index.
    
    Args:
        index (int): The index of the obligation.
    
    Returns:
        dict: A dictionary containing the obligation details.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {
            "party": result[0],
            "description": result[1],
            "deadline": result[2],
            "penalty": result[3],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def acknowledgeObligation(index):
    """Acknowledge an obligation by index.
    
    Args:
        index (int): The index of the obligation to acknowledge.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.acknowledgeObligation(index).buildTransaction({
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
def makePayment(paymentAmount):
    """Make a payment to the contract.
    
    Args:
        paymentAmount (int): The amount to be paid.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.makePayment(paymentAmount).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(paymentAmount, 'ether')
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()