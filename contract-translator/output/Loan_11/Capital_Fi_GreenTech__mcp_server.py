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
def checkObligation():
    """Check the borrower's obligation status.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.checkObligation().buildTransaction({
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
def makePayment(amount: int):
    """Make a payment towards the loan.
    
    Args:
        amount (int): The amount of the payment.
        
    Returns:
        dict: A dictionary containing the transaction hash.
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
def getBorrower():
    """Get the address of the borrower.
    
    Returns:
        dict: A dictionary containing the borrower's address.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrowerObligation():
    """Get the borrower's obligation.
    
    Returns:
        dict: A dictionary containing the borrower's obligation.
    """
    try:
        result = contract.functions.getBorrowerObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrowerObligationPenalty():
    """Get the penalty associated with the borrower's obligation.
    
    Returns:
        dict: A dictionary containing the borrower's obligation penalty.
    """
    try:
        result = contract.functions.getBorrowerObligationPenalty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisbursementDate():
    """Get the disbursement date of the loan.
    
    Returns:
        dict: A dictionary containing the disbursement date as a timestamp.
    """
    try:
        result = contract.functions.getDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDueDate():
    """Get the due date for the first payment.
    
    Returns:
        dict: A dictionary containing the first payment due date as a timestamp.
    """
    try:
        result = contract.functions.getFirstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanAmount():
    """Get the amount of the loan.
    
    Returns:
        dict: A dictionary containing the loan amount.
    """
    try:
        result = contract.functions.getLoanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLender():
    """Get the address of the lender.
    
    Returns:
        dict: A dictionary containing the lender's address.
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPaymentAmount():
    """Get the amount due for monthly payments.
    
    Returns:
        dict: A dictionary containing the monthly payment amount.
    """
    try:
        result = contract.functions.getMonthlyPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getOriginationFeeAmount():
    """Get the origination fee amount.
    
    Returns:
        dict: A dictionary containing the origination fee amount.
    """
    try:
        result = contract.functions.getOriginationFeeAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Get the start date of the loan agreement.
    
    Returns:
        dict: A dictionary containing the start date as a timestamp.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDefaultInterestRate():
    """Get the default interest rate associated with the loan.
    
    Returns:
        dict: A dictionary containing the default interest rate.
    """
    try:
        result = contract.functions.getDefaultInterestRate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def initializeAgreement(_lender: str, _borrower: str, _loanAmount: int, _monthlyPayment: int,
                        _originationFee: int, _startDate: int, _disbursementDate: int,
                        _firstPaymentDueDate: int, _borrowerObligation: str,
                        _borrowerObligationPenalty: str, _defaultInterestRate: int,
                        _defaultAcceleration: str):
    """Initialize the loan agreement with the specified parameters.
    
    Args:
        _lender (str): The address of the lender.
        _borrower (str): The address of the borrower.
        _loanAmount (int): The loan amount.
        _monthlyPayment (int): The monthly payment amount.
        _originationFee (int): The origination fee.
        _startDate (int): The start date of the agreement.
        _disbursementDate (int): The disbursement date of the loan.
        _firstPaymentDueDate (int): The due date for the first payment.
        _borrowerObligation (str): Obligations of the borrower.
        _borrowerObligationPenalty (str): Penalty in case of obligation breach.
        _defaultInterestRate (int): Default interest rate.
        _defaultAcceleration (str): Default acceleration clause.
        
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.initializeAgreement(
            Web3.to_checksum_address(_lender),
            Web3.to_checksum_address(_borrower),
            _loanAmount,
            _monthlyPayment,
            _originationFee,
            _startDate,
            _disbursementDate,
            _firstPaymentDueDate,
            _borrowerObligation,
            _borrowerObligationPenalty,
            _defaultInterestRate,
            _defaultAcceleration
        ).buildTransaction({
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