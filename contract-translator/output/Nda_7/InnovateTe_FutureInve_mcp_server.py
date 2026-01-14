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
def updateObligation(_description: str, _penalty: str) -> dict:
    """
    Updates the obligation of the NDA.

    :param _description: Description of the obligation.
    :param _penalty: Penalty for breach of obligation.
    :return: Transaction hash or error.
    """
    try:
        txn = contract.functions.updateObligation(_description, _penalty).buildTransaction({
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
def terminateAgreement() -> dict:
    """
    Terminates the NDA agreement.

    :return: Transaction hash or error.
    """
    try:
        txn = contract.functions.terminateAgreement().buildTransaction({
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
def getNDAInfo() -> dict:
    """
    Retrieves the details of the NDA.

    :return: NDA information or error.
    """
    try:
        result = contract.functions.getNDAInfo().call()
        return {
            "description": result[0],
            "penalty": result[1],
            "state": result[2],
            "startDate": result[3],
            "endDate": result[4],
            "disclosingParty": result[5],
            "receivingParty": result[6],
            "obligationDesc": result[7],
            "obligationPenalty": result[8]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def disclosingParty() -> dict:
    """
    Retrieves the details of the disclosing party.

    :return: Disclosing party information or error.
    """
    try:
        result = contract.functions.disclosingParty().call()
        return {
            "name": result[0],
            "role": result[1],
            "addr": result[2],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def receivingParty() -> dict:
    """
    Retrieves the details of the receiving party.

    :return: Receiving party information or error.
    """
    try:
        result = contract.functions.receivingParty().call()
        return {
            "name": result[0],
            "role": result[1],
            "addr": result[2],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def obligation() -> dict:
    """
    Retrieves the current obligation details.

    :return: Obligation information or error.
    """
    try:
        result = contract.functions.obligation().call()
        return {
            "description": result[0],
            "penaltyForBreach": result[1],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def state() -> dict:
    """
    Retrieves the current state of the NDA agreement.

    :return: Current state as a uint8 value or error.
    """
    try:
        result = contract.functions.state().call()
        return {"state": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def startDate() -> dict:
    """
    Retrieves the start date of the NDA agreement.

    :return: Start date as a uint256 value or error.
    """
    try:
        result = contract.functions.startDate().call()
        return {"startDate": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def endDate() -> dict:
    """
    Retrieves the end date of the NDA agreement.

    :return: End date as a uint256 value or error.
    """
    try:
        result = contract.functions.endDate().call()
        return {"endDate": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()