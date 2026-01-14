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
def makePayment(amount: int):
    """
    Makes a payment on the loan.

    :param amount: The amount to be paid.
    :return: Transaction hash in case of success or error message.
    """
    try:
        txn = contract.functions.makePayment(amount).buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation():
    """
    Fulfills the obligation under the loan contract.

    :return: Transaction hash in case of success or error message.
    """
    try:
        txn = contract.functions.fulfillObligation().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLender():
    """
    Retrieves the address of the lender.

    :return: Lender's address.
    """
    try:
        result = contract.functions.getLender().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrower():
    """
    Retrieves the address of the borrower.

    :return: Borrower's address.
    """
    try:
        result = contract.functions.getBorrower().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanAmount():
    """
    Retrieves the total loan amount.

    :return: Total loan amount.
    """
    try:
        result = contract.functions.getLoanAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPayment():
    """
    Retrieves the monthly payment amount.

    :return: Monthly payment amount.
    """
    try:
        result = contract.functions.getMonthlyPayment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLatePaymentFee():
    """
    Retrieves the late payment fee.

    :return: Late payment fee amount.
    """
    try:
        result = contract.functions.getLatePaymentFee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getLoanStartDate():
    """
    Retrieves the loan start date.

    :return: Loan start date as a timestamp.
    """
    try:
        result = contract.functions.getLoanStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisbursementDate():
    """
    Retrieves the disbursement date of the loan.

    :return: Disbursement date as a timestamp.
    """
    try:
        result = contract.functions.getDisbursementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFirstPaymentDate():
    """
    Retrieves the first payment date.

    :return: First payment date as a timestamp.
    """
    try:
        result = contract.functions.getFirstPaymentDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBorrowerObligation():
    """
    Retrieves the borrower's obligation details.

    :return: Borrower's obligation as a string.
    """
    try:
        result = contract.functions.getBorrowerObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDefaultInterestRate():
    """
    Retrieves the default interest rate for the loan.

    :return: Default interest rate as a string.
    """
    try:
        result = contract.functions.getDefaultInterestRate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getAccelerationTerm():
    """
    Retrieves the acceleration term for the loan.

    :return: Acceleration term as a string.
    """
    try:
        result = contract.functions.getAccelerationTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDefaultTriggers():
    """
    Retrieves the default triggers associated with the loan.

    :return: List of default triggers as strings.
    """
    try:
        result = contract.functions.getDefaultTriggers().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()