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
abi_path = Path(__file__).parent / 'TechCorp_I_Robert_Joh.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("TechCorp_I_Robert_Joh")

@mcp.tool()
def releasePayment(amount: int, currency: str):
    """
    Releases payment to the employee.

    Who can call it: Employer
    Parameters:
    - amount (int): The payment amount to release.
    - currency (str): The currency in which the payment is made.

    Returns:
    - dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.releasePayment(amount, currency).buildTransaction({
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
def terminateEmployment(reason: str):
    """
    Terminates the employment contract.

    Who can call it: Employer
    Parameters:
    - reason (str): The reason for termination.

    Returns:
    - dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.terminateEmployment(reason).buildTransaction({
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
def getFinancialTerms():
    """
    Retrieves the financial terms of the employment contract.

    Who can call it: Anyone
    Returns:
    - dict: The financial terms.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """
    Retrieves the obligations of both parties in the employment contract.

    Who can call it: Anyone
    Returns:
    - dict: The obligations of each party.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """
    Retrieves any special terms of the employment contract.

    Who can call it: Anyone
    Returns:
    - dict: The special terms as a list of strings.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """
    Retrieves the conditions under which employment can be terminated.

    Who can call it: Anyone
    Returns:
    - dict: The termination conditions as a list of strings.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()