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
def confirmConfidentiality():
    """
    Checks if the confidentiality has been confirmed.

    Returns:
        dict: {"result": bool} indicating whether confidentiality is confirmed.
    """
    try:
        result = contract.functions.confirmConfidentiality().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def reportBreach():
    """
    Reports a breach of the NDA.

    Returns:
        dict: {"tx_hash": hash} of the transaction that reported the breach.
    """
    try:
        txn = contract.functions.reportBreach().buildTransaction({
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
def calculatePenalty():
    """
    Calculates the penalty for breach of the NDA.

    Returns:
        dict: {"result": uint256} indicating the calculated penalty.
    """
    try:
        result = contract.functions.calculatePenalty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConfidentialParties():
    """
    Retrieves the addresses of the confidential parties involved in the NDA.

    Returns:
        dict: {"result": list} of addresses of confidential parties.
    """
    try:
        result = contract.functions.getConfidentialParties().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()