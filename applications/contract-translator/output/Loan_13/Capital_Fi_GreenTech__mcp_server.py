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
    """
    Retrieve lender information.

    Returns:
        dict: A dictionary containing lender's details: name, address.
    """
    try:
        lender_info = contract.functions.getLender().call()
        return {"name": lender_info[0], "contact": lender_info[1], "address": lender_info[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """
    Retrieve borrower information.

    Returns:
        dict: A dictionary containing borrower's details: name, address.
    """
    try:
        borrower_info = contract.functions.getBorrower().call()
        return {"name": borrower_info[0], "contact": borrower_info[1], "address": borrower_info[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index):
    """
    Retrieve financial terms by index.

    Parameters:
        index (int): The index of the financial term.

    Returns:
        dict: A dictionary containing the financial term details.
    """
    try:
        financial_term = contract.functions.getFinancialTerm(index).call()
        return {
            "term_length": financial_term[0],
            "interest_rate": financial_term[1],
            "payment_schedule": financial_term[2],
            "term_type": financial_term[3],
            "term_description": financial_term[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDateInfo(index):
    """
    Retrieve date information related to the term.

    Parameters:
        index (int): The index for the date information.

    Returns:
        dict: A dictionary containing date-related details.
    """
    try:
        date_info = contract.functions.getDateInfo(index).call()
        return {
            "start_date": date_info[0],
            "end_date": date_info[1],
            "duration": date_info[2],
            "date_type": date_info[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """
    Retrieve obligation details by index.

    Parameters:
        index (int): The index of the obligation.

    Returns:
        dict: A dictionary containing obligation details.
    """
    try:
        obligation_info = contract.functions.getObligation(index).call()
        return {
            "description": obligation_info[0],
            "responsibility": obligation_info[1],
            "penalties": obligation_info[2],
            "obligation_type": obligation_info[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDefaultInterestRate():
    """
    Retrieve the default interest rate.

    Returns:
        dict: A dictionary containing the default interest rate.
    """
    try:
        default_interest_rate = contract.functions.getDefaultInterestRate().call()
        return {"default_interest_rate": default_interest_rate}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makePayment(amount):
    """
    Make a payment towards the loan.

    Parameters:
        amount (int): The amount to be paid.

    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.makePayment(amount).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(amount, 'ether')  # Assuming amount is in ether
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(index):
    """
    Fulfill a specific obligation.

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

if __name__ == "__main__":
    mcp.run()