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
def updateObligation(_description: str, _penaltyForBreach: str):
    """Update the obligation details of the NDA.
    
    Parameters:
        _description (str): Description of the obligation.
        _penaltyForBreach (str): Penalty for breach of obligation.
    
    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.updateObligation(_description, _penaltyForBreach).buildTransaction({
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
def reportConfidentialityBreach(details: str):
    """Report a breach of confidentiality.
    
    Parameters:
        details (str): Details of the breach.
    
    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.reportConfidentialityBreach(details).buildTransaction({
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
def getNdaDetails():
    """Retrieve the details of the NDA.
    
    Returns:
        dict: NDA details including parties and obligations or error message.
    """
    try:
        result = contract.functions.getNdaDetails().call()
        return {
            "disclosing_party": result[0],
            "receiving_party": result[1],
            "dates": {
                "startDate": result[2][0],
                "confidentialityPeriodEnd": result[2][1]
            },
            "obligation": {
                "description": result[3][0],
                "penaltyForBreach": result[3][1]
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()