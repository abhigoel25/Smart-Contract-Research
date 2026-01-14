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
    """Returns the lender's details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing lender's details.
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Returns the borrower's details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing borrower's details.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanTerm():
    """Returns the loan term details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing the loan term details.
    """
    try:
        result = contract.functions.getLoanTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPaymentTerm():
    """Returns the monthly payment term details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing monthly payment term details.
    """
    try:
        result = contract.functions.getMonthlyPaymentTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getOriginationFeeTerm():
    """Returns the origination fee term details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing origination fee term details.
    """
    try:
        result = contract.functions.getOriginationFeeTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLatePaymentFeeTerm():
    """Returns the late payment fee term details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing late payment fee term details.
    """
    try:
        result = contract.functions.getLatePaymentFeeTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Returns the loan start date details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing start date details.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisbursementDate():
    """Returns the loan disbursement date details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing disbursement date details.
    """
    try:
        result = contract.functions.getDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDueDate():
    """Returns the first payment due date details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing first payment due date details.
    """
    try:
        result = contract.functions.getFirstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEndDate():
    """Returns the loan end date details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing end date details.
    """
    try:
        result = contract.functions.getEndDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation():
    """Returns the loan obligation details.
    
    This function can be called by anyone.
    
    Returns:
        dict: A dictionary containing obligation details.
    """
    try:
        result = contract.functions.getObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makePayment(amount: int):
    """Makes a payment towards the loan.
    
    This function should be called by the borrower and requires the payment amount.
    
    Args:
        amount (int): The amount to be paid.
    
    Returns:
        dict: A dictionary containing the transaction hash of the payment.
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

@mcp.tool()
def fulfillObligation():
    """Fulfills the loan obligation.
    
    This function should be called by the borrower.
    
    Returns:
        dict: A dictionary containing the transaction hash of fulfilling the obligation.
    """
    try:
        txn = contract.functions.fulfillObligation().buildTransaction({
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