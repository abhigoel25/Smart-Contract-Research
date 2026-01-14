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
    """Returns the address of the lender."""
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """Returns the address of the borrower."""
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanAmount():
    """Returns the total loan amount."""
    try:
        result = contract.functions.getLoanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPayment():
    """Returns the monthly payment amount."""
    try:
        result = contract.functions.getMonthlyPayment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getOriginationFee():
    """Returns the origination fee for the loan."""
    try:
        result = contract.functions.getOriginationFee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanDisbursementDate():
    """Returns the loan disbursement date."""
    try:
        result = contract.functions.getLoanDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDueDate():
    """Returns the first payment due date."""
    try:
        result = contract.functions.getFirstPaymentDueDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanTermStartDate():
    """Returns the loan term start date."""
    try:
        result = contract.functions.getLoanTermStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """Returns details of the obligation for the given index.
    
    Parameters:
    - index: Index of the obligation.
    """
    try:
        description, deadline, penalty = contract.functions.getObligation(index).call()
        return {"description": description, "deadline": deadline, "penalty": penalty}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationCondition(index):
    """Returns the termination condition for the given obligation index.
    
    Parameters:
    - index: Index of the termination condition.
    """
    try:
        result = contract.functions.getTerminationCondition(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def performObligation(index):
    """Performs the obligation for the given index.
    
    Parameters:
    - index: Index of the obligation to perform.
    """
    try:
        txn = contract.functions.performObligation(index).buildTransaction({
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
def makeMonthlyPayment():
    """Makes the monthly payment for the loan."""
    try:
        txn = contract.functions.makeMonthlyPayment().buildTransaction({
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
    """Disburses the loan."""
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

if __name__ == "__main__":
    mcp.run()