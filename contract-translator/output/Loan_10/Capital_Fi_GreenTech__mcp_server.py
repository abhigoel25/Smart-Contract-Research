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
    """Fetches the lender's information.
    
    Returns:
        dict: Contains lender details including name and address.
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Fetches the borrower's information.
    
    Returns:
        dict: Contains borrower details including name and address.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanDetails():
    """Retrieves the loan details.
    
    Returns:
        dict: Contains details about the loan such as amount and terms.
    """
    try:
        result = contract.functions.getLoanDetails().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPaymentDetails():
    """Retrieves details of the monthly payment.
    
    Returns:
        dict: Contains information about the monthly payment.
    """
    try:
        result = contract.functions.getMonthlyPaymentDetails().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getOriginationFeeDetails():
    """Fetches the origination fee details.
    
    Returns:
        dict: Contains information about the origination fee.
    """
    try:
        result = contract.functions.getOriginationFeeDetails().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getExecutionDate():
    """Retrieves the loan execution date.
    
    Returns:
        dict: Contains the execution date details.
    """
    try:
        result = contract.functions.getExecutionDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisbursementDate():
    """Retrieves the loan disbursement date.
    
    Returns:
        dict: Contains the disbursement date details.
    """
    try:
        result = contract.functions.getDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDueDate():
    """Retrieves the first payment due date.
    
    Returns:
        dict: Contains the first payment due date details.
    """
    try:
        result = contract.functions.getFirstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligationCount():
    """Fetches the number of obligations.
    
    Returns:
        dict: Contains the count of obligations.
    """
    try:
        result = contract.functions.getObligationCount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """Retrieves a specific obligation by index.
    
    Parameters:
        index (uint256): The index of the obligation.

    Returns:
        dict: Contains details of the specific obligation.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """Fetches the special terms of the loan.
    
    Returns:
        dict: Contains an array of special terms.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """Retrieves the termination conditions of the loan.
    
    Returns:
        dict: Contains an array of termination conditions.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def performLoanDisbursement():
    """Initiates the loan disbursement process.
    
    Returns:
        dict: Transaction hash of the disbursement.
    """
    try:
        txn = contract.functions.performLoanDisbursement().buildTransaction({
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
    """Makes a payment towards the loan.
    
    Parameters:
        amount (uint256): The amount to be paid.

    Returns:
        dict: Transaction hash of the payment.
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