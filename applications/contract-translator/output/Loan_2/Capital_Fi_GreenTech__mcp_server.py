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
def checkDefault():
    """Check if a default has occurred on the loan.
    
    Returns:
        dict: {'tx_hash': transaction hash} or {'error': str}
    """
    try:
        txn = contract.functions.checkDefault().buildTransaction({
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
def disburseLoan():
    """Disburse the loan to the borrower.
    
    Returns:
        dict: {'tx_hash': transaction hash} or {'error': str}
    """
    try:
        txn = contract.functions.disburseLoan().buildTransaction({
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
def insuranceMaintained():
    """Check if the insurance is maintained.
    
    Returns:
        dict: {'result': bool}
    """
    try:
        result = contract.functions.insuranceMaintained().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def loanRepaid():
    """Check if the loan has been repaid.
    
    Returns:
        dict: {'result': bool}
    """
    try:
        result = contract.functions.loanRepaid().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def loanAmount():
    """Get the amount of the loan.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.loanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def monthlyPayment():
    """Get the amount of the monthly payment.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.monthlyPayment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def originationFee():
    """Get the origination fee for the loan.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.originationFee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def paymentsMade():
    """Get the number of payments made.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.paymentsMade().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def totalPayments():
    """Get the total number of payments.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.totalPayments().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def terminateContract():
    """Terminate the loan contract.
    
    Returns:
        dict: {'tx_hash': transaction hash} or {'error': str}
    """
    try:
        txn = contract.functions.terminateContract().buildTransaction({
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
def markInsurance(status: bool):
    """Mark the insurance status for the loan.
    
    Args:
        status (bool): Insurance status to be set.

    Returns:
        dict: {'tx_hash': transaction hash} or {'error': str}
    """
    try:
        txn = contract.functions.markInsurance(status).buildTransaction({
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
def borrower():
    """Get the address of the borrower.
    
    Returns:
        dict: {'result': address}
    """
    try:
        result = contract.functions.borrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def lender():
    """Get the address of the lender.
    
    Returns:
        dict: {'result': address}
    """
    try:
        result = contract.functions.lender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def loanStartDate():
    """Get the loan start date.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.loanStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def loanDisbursementDate():
    """Get the loan disbursement date.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.loanDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def firstPaymentDueDate():
    """Get the date of the first payment due.
    
    Returns:
        dict: {'result': uint256}
    """
    try:
        result = contract.functions.firstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()