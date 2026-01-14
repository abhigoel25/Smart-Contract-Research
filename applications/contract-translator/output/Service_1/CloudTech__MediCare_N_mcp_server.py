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
abi_path = Path(__file__).parent / 'CloudTech__MediCare_N.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("CloudTech__MediCare_N")

@mcp.tool()
def getFinancialTerms():
    """ 
    Retrieve the financial terms of the service agreement.
    
    Returns:
        dict: Contains an array of financial terms.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """ 
    Retrieve the obligations of the agreement.
    
    Returns:
        dict: Contains an array of obligations.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerm():
    """ 
    Retrieve the term details of the service agreement.
    
    Returns:
        dict: Contains the term start and end date.
    """
    try:
        result = contract.functions.getTerm().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def paySetupFee():
    """ 
    Pay the setup fee for the service agreement.
    
    Returns:
        dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.paySetupFee().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(0.1, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payMonthlyFee():
    """ 
    Pay the monthly fee for the service agreement.
    
    Returns:
        dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.payMonthlyFee().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(0.05, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(obligationIndex):
    """ 
    Fulfill an obligation at the specified index in the agreement.
    
    Parameters:
        obligationIndex (uint256): The index of the obligation to fulfill.
    
    Returns:
        dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.fulfillObligation(obligationIndex).buildTransaction({
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
def terminateAgreement(reason):
    """ 
    Terminate the service agreement with a given reason.
    
    Parameters:
        reason (string): The reason for termination.
    
    Returns:
        dict: Contains the transaction hash.
    """
    try:
        txn = contract.functions.terminateAgreement(reason).buildTransaction({
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