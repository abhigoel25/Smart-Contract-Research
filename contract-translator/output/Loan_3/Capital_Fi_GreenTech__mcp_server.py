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
def makePayment(amount: int) -> dict:
    """
    Make a payment towards the loan.

    Parameters:
    - amount (int): The amount to pay.

    Returns:
    - dict: Transaction hash if successful, error message if failed.
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
def triggerDefault() -> dict:
    """
    Trigger a default on the loan.

    Returns:
    - dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.triggerDefault().buildTransaction({
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
def getLoanDetails() -> dict:
    """
    Get the loan details.

    Returns:
    - dict: Loan details including lender, borrower, loan amount, and monthly payment.
    """
    try:
        result = contract.functions.getLoanDetails().call()
        return {
            "lender": result[0],
            "borrower": result[1],
            "loan_amount": result[2],
            "monthly_payment": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations() -> dict:
    """
    Get the loan obligations.

    Returns:
    - dict: The obligations associated with the loan.
    """
    try:
        result = contract.functions.getObligations().call()
        return {
            "obligation1": result[0],
            "obligation2": result[1]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def lender() -> dict:
    """
    Get the lender's address.

    Returns:
    - dict: The address of the lender.
    """
    try:
        result = contract.functions.lender().call()
        return {"lender": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def borrower() -> dict:
    """
    Get the borrower's address.

    Returns:
    - dict: The address of the borrower.
    """
    try:
        result = contract.functions.borrower().call()
        return {"borrower": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def loanAmount() -> dict:
    """
    Get the loan amount.

    Returns:
    - dict: The loan amount.
    """
    try:
        result = contract.functions.loanAmount().call()
        return {"loan_amount": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def monthlyPayment() -> dict:
    """
    Get the monthly payment amount.

    Returns:
    - dict: The monthly payment amount.
    """
    try:
        result = contract.functions.monthlyPayment().call()
        return {"monthly_payment": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def originationFee() -> dict:
    """
    Get the origination fee.

    Returns:
    - dict: The origination fee amount.
    """
    try:
        result = contract.functions.originationFee().call()
        return {"origination_fee": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def latePaymentFeePercent() -> dict:
    """
    Get the late payment fee percentage.

    Returns:
    - dict: The late payment fee percentage.
    """
    try:
        result = contract.functions.latePaymentFeePercent().call()
        return {"late_payment_fee_percent": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def isActive() -> dict:
    """
    Check if the loan is active.

    Returns:
    - dict: Boolean indicating if the loan is active.
    """
    try:
        result = contract.functions.isActive().call()
        return {"is_active": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()