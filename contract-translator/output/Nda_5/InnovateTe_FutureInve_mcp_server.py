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
def updateObligationStatus(obligationId: int, status: int):
    """
    Update the status of an obligation.

    :param obligationId: Unique identifier for the obligation.
    :param status: New status to set for the obligation.
    :return: Transaction hash.
    """
    try:
        txn = contract.functions.updateObligationStatus(obligationId, status).buildTransaction({
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
def terminateContract():
    """
    Terminate the NDA contract.

    :return: Transaction hash.
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
def getObligation(obligationId: int):
    """
    Retrieve the details of an obligation.

    :param obligationId: Unique identifier for the obligation.
    :return: Details of the obligation including description, status, and penalty for breach.
    """
    try:
        description, status, penaltyForBreach = contract.functions.getObligation(obligationId).call()
        return {
            "description": description,
            "status": status,
            "penaltyForBreach": penaltyForBreach
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """
    Retrieve the special terms of the NDA contract.

    :return: Special terms, conditions, and termination conditions.
    """
    try:
        terms, conditions, terminationConditions = contract.functions.getSpecialTerms().call()
        return {
            "terms": terms,
            "conditions": conditions,
            "terminationConditions": terminationConditions
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()