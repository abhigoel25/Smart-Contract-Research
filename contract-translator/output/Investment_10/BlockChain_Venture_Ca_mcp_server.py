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
abi_path = Path(__file__).parent / 'BlockChain_Venture_Ca.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def getParty(index: int):
    """Gets the details of a party in the investment contract.
    
    Args:
        index (int): The index of the party.

    Returns:
        dict: Contains party details including name, role, address, email, and entity type.
    """
    try:
        result = contract.functions.getParty(index).call()
        return {
            "name": result[0],
            "role": result[1],
            "address": result[2],
            "email": result[3],
            "entityType": result[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index: int):
    """Gets the financial terms related to the investment.

    Args:
        index (int): The index of the financial term.

    Returns:
        dict: Contains the financial term details including amount, currency, purpose, frequency, and due date.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {
            "amount": result[0],
            "currency": result[1],
            "purpose": result[2],
            "frequency": result[3],
            "dueDate": result[4]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDateInfo(index: int):
    """Gets date information related to the investment.

    Args:
        index (int): The index for the date information.

    Returns:
        dict: Contains date info including type, value, day of month, and frequency.
    """
    try:
        result = contract.functions.getDateInfo(index).call()
        return {
            "dateType": result[0],
            "value": result[1],
            "dayOfMonth": result[2],
            "frequency": result[3]
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation(index: int):
    """Fulfill an obligation in the investment contract.

    Args:
        index (int): The index of the obligation to fulfill.

    Returns:
        dict: Transaction hash upon successful execution.
    """
    try:
        txn = contract.functions.fulfillObligation(index).buildTransaction({
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
def executeInvestment():
    """Execute the investment in the contract.

    Returns:
        dict: Transaction hash upon successful execution.
    """
    try:
        txn = contract.functions.executeInvestment().buildTransaction({
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