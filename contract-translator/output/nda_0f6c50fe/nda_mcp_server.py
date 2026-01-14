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
abi_path = Path(__file__).parent / 'nda.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("InnovateTe_FutureInve")

@mcp.tool()
def confirmConfidentiality():
    """
    Confirms confidentiality obligations as defined in the NDA.

    Returns:
        dict: Contains the transaction hash of the executed function.
    """
    try:
        txn = contract.functions.confirmConfidentiality().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def reportBreach():
    """
    Reports a breach of confidentiality as specified in the NDA.

    Returns:
        dict: Contains the transaction hash of the executed function.
    """
    try:
        txn = contract.functions.reportBreach().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def calculatePenalty():
    """
    Calculates the penalty associated with a breach of the NDA.

    Returns:
        dict: Contains the penalty amount.
    """
    try:
        result = contract.functions.calculatePenalty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def checkTermEnd():
    """
    Checks if the term of the NDA has ended.

    Returns:
        dict: Contains the transaction hash of the executed function.
    """
    try:
        txn = contract.functions.checkTermEnd().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()