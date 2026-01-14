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
    """Retrieve the address of the lender.
    
    Returns:
        dict: {"result": address of lender}
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Retrieve the address of the borrower.
    
    Returns:
        dict: {"result": address of borrower}
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanAmount():
    """Retrieve the loan amount.
    
    Returns:
        dict: {"result": loan amount}
    """
    try:
        result = contract.functions.getLoanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPaymentAmount():
    """Retrieve the monthly payment amount.
    
    Returns:
        dict: {"result": monthly payment amount}
    """
    try:
        result = contract.functions.getMonthlyPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getOriginationFeeAmount():
    """Retrieve the origination fee amount.
    
    Returns:
        dict: {"result": origination fee amount}
    """
    try:
        result = contract.functions.getOriginationFeeAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Retrieve the start date of the loan.
    
    Returns:
        dict: {"result": start date}
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisbursementDate():
    """Retrieve the disbursement date of the loan.
    
    Returns:
        dict: {"result": disbursement date}
    """
    try:
        result = contract.functions.getDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDueDate():
    """Retrieve the first payment due date.
    
    Returns:
        dict: {"result": first payment due date}
    """
    try:
        result = contract.functions.getFirstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTermEndDate():
    """Retrieve the term end date of the loan.
    
    Returns:
        dict: {"result": term end date}
    """
    try:
        result = contract.functions.getTermEndDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def maintainInsurance():
    """Maintain the insurance on the loan.
    
    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.maintainInsurance().buildTransaction({
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
def prepayLoan():
    """Prepay the loan.
    
    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.prepayLoan().buildTransaction({
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
def setDefaultConditions(triggers, acceleration, interestRate):
    """Set the default conditions for the loan.
    
    Args:
        triggers (str): Trigger conditions.
        acceleration (str): Acceleration conditions.
        interestRate (str): Interest rate conditions.

    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.setDefaultConditions(triggers, acceleration, interestRate).buildTransaction({
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
def getDefaultConditions():
    """Retrieve the default conditions set for the loan.
    
    Returns:
        dict: {"result": tuple of (triggers, acceleration, interestRate)}
    """
    try:
        result = contract.functions.getDefaultConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setDisbursementDate(_disbursementDate):
    """Set the disbursement date for the loan.
    
    Args:
        _disbursementDate (uint256): Disbursement date timestamp.

    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.setDisbursementDate(_disbursementDate).buildTransaction({
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
def setFirstPaymentDueDate(_firstPaymentDueDate):
    """Set the first payment due date for the loan.
    
    Args:
        _firstPaymentDueDate (uint256): First payment due date timestamp.

    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.setFirstPaymentDueDate(_firstPaymentDueDate).buildTransaction({
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
def setTermEndDate(_termEndDate):
    """Set the term end date for the loan.
    
    Args:
        _termEndDate (uint256): Term end date timestamp.

    Returns:
        dict: {"tx_hash": transaction hash}
    """
    try:
        txn = contract.functions.setTermEndDate(_termEndDate).buildTransaction({
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