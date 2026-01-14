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
abi_path = Path(__file__).parent / 'Michael_Ch_Jessica_Wi.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("Michael_Ch_Jessica_Wi")

@mcp.tool()
def addFinancialTerm(amount: int, currency: str, purpose: str, frequency: str):
    """Adds a financial term to the partnership.

    Args:
        amount (int): The amount of the financial term.
        currency (str): The currency of the financial term.
        purpose (str): The purpose of the financial term.
        frequency (str): The frequency of the financial term.

    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.addFinancialTerm(amount, currency, purpose, frequency).buildTransaction({
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
def contributeCapital(index: int):
    """Contributes capital to the partnership.

    Args:
        index (int): The index of the partner contributing capital.

    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.contributeCapital(index).buildTransaction({
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
def assignObligation(party: str, description: str):
    """Assigns an obligation to a partner.

    Args:
        party (str): The name of the party receiving the obligation.
        description (str): Description of the obligation.

    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.assignObligation(party, description).buildTransaction({
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
def addAsset(assetType: str, description: str):
    """Adds an asset to the partnership.

    Args:
        assetType (str): The type of the asset.
        description (str): A description of the asset.

    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.addAsset(assetType, description).buildTransaction({
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
def getPartners():
    """Fetches the list of partners in the partnership.

    Returns:
        dict: List of partner addresses.
    """
    try:
        result = contract.functions.getPartners().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerms():
    """Fetches the financial terms of the partnership.

    Returns:
        dict: List of financial terms.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """Fetches the obligations of the partnership.

    Returns:
        dict: List of obligations.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getAssets():
    """Fetches the assets of the partnership.

    Returns:
        dict: List of assets.
    """
    try:
        result = contract.functions.getAssets().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def withdrawMembership():
    """Withdraws a member from the partnership.

    Returns:
        dict: Transaction hash or error message.
    """
    try:
        txn = contract.functions.withdrawMembership().buildTransaction({
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