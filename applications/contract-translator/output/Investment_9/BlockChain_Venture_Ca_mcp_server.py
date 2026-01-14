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
def getParty(partyAddress: str):
    """
    Retrieve information about a party involved in the investment.
    
    Parameters:
        partyAddress (str): The blockchain address of the party.
        
    Returns:
        dict: Contains name, role, email, and entityType of the party.
    """
    try:
        result = contract.functions.getParty(Web3.to_checksum_address(partyAddress)).call()
        return {"name": result[0], "role": result[1], "email": result[2], "entityType": result[3]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getFinancialTerm(index: int):
    """
    Retrieve financial term details by index.
    
    Parameters:
        index (int): The index of the financial term.
        
    Returns:
        dict: Contains amount, currency, and purpose of the financial term.
    """
    try:
        result = contract.functions.getFinancialTerm(index).call()
        return {"amount": result[0], "currency": result[1], "purpose": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDate(index: int):
    """
    Retrieve date information by index.
    
    Parameters:
        index (int): The index of the date.
        
    Returns:
        dict: Contains dateType and value of the date.
    """
    try:
        result = contract.functions.getDate(index).call()
        return {"dateType": result[0], "value": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getAsset(index: int):
    """
    Retrieve asset information by index.
    
    Parameters:
        index (int): The index of the asset.
        
    Returns:
        dict: Contains assetType, description, quantity, and value of the asset.
    """
    try:
        result = contract.functions.getAsset(index).call()
        return {"assetType": result[0], "description": result[1], "quantity": result[2], "value": result[3]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index: int):
    """
    Retrieve obligation information by index.
    
    Parameters:
        index (int): The index of the obligation.
        
    Returns:
        dict: Contains party, description, and deadline of the obligation.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {"party": result[0], "description": result[1], "deadline": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def executeInvestment(index: int):
    """
    Execute an investment based on the given index.
    
    Parameters:
        index (int): The index of the investment to execute.
        
    Returns:
        dict: Contains transaction hash.
    """
    try:
        txn = contract.functions.executeInvestment(index).buildTransaction({
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
def fulfillObligation(index: int):
    """
    Fulfill an obligation based on the given index.
    
    Parameters:
        index (int): The index of the obligation to fulfill.
        
    Returns:
        dict: Contains transaction hash.
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

if __name__ == "__main__":
    mcp.run()