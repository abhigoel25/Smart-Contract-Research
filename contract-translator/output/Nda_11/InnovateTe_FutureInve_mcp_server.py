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
abi_path = Path(__file__).parent / 'InnovateTe_FutureInve.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("InnovateTe_FutureInve")

@mcp.tool()
def confirmConfidentiality(party: str) -> dict:
    """
    Confirm confidentiality for a party.
    
    Parameters:
    - party (str): The address of the party confirming confidentiality.
    
    Returns:
    - dict: Transaction hash if successful, or error message.
    """
    try:
        txn = contract.functions.confirmConfidentiality(Web3.to_checksum_address(party)).buildTransaction({
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
def reportBreach(party: str) -> dict:
    """
    Report a breach by a specific party.
    
    Parameters:
    - party (str): The address of the party reporting the breach.
    
    Returns:
    - dict: Transaction hash if successful, or error message.
    """
    try:
        txn = contract.functions.reportBreach(Web3.to_checksum_address(party)).buildTransaction({
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
def calculatePenalty() -> dict:
    """
    Calculate the breach penalty.
    
    Returns:
    - dict: The calculated penalty.
    """
    try:
        result = contract.functions.calculatePenalty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConfidentialParties() -> dict:
    """
    Get the list of parties that have confirmed confidentiality.
    
    Returns:
    - dict: The list of confidential parties' addresses.
    """
    try:
        result = contract.functions.getConfidentialParties().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()