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
def getDisclosingParty():
    """Fetch the disclosing party details.
    
    Returns:
        dict: A dictionary containing party name and address.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"party": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Fetch the receiving party details.
    
    Returns:
        dict: A dictionary containing party name and address.
    """
    try:
        result = contract.functions.getReceivingParty().call()
        return {"party": result[0], "address": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Fetch the start date of the NDA.
    
    Returns:
        dict: A dictionary containing the start date as a timestamp.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"start_date": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEndDate():
    """Fetch the end date of the NDA.
    
    Returns:
        dict: A dictionary containing the end date as a timestamp.
    """
    try:
        result = contract.functions.getEndDate().call()
        return {"end_date": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation(index):
    """Fetch an obligation by index.
    
    Args:
        index (uint256): The index of the obligation to fetch.
        
    Returns:
        dict: A dictionary containing the obligation details.
    """
    try:
        result = contract.functions.getObligation(index).call()
        return {"party": result[0], "description": result[1], "penalty_for_breach": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligationCount():
    """Fetch the total count of obligations.
    
    Returns:
        dict: A dictionary containing the obligation count.
    """
    try:
        result = contract.functions.getObligationCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerm(index):
    """Fetch a special term by index.
    
    Args:
        index (uint256): The index of the special term to fetch.
        
    Returns:
        dict: A dictionary containing the special term.
    """
    try:
        result = contract.functions.getSpecialTerm(index).call()
        return {"term": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTermCount():
    """Fetch the total count of special terms.
    
    Returns:
        dict: A dictionary containing the special term count.
    """
    try:
        result = contract.functions.getSpecialTermCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationCondition(index):
    """Fetch a termination condition by index.
    
    Args:
        index (uint256): The index of the termination condition to fetch.
        
    Returns:
        dict: A dictionary containing the termination condition.
    """
    try:
        result = contract.functions.getTerminationCondition(index).call()
        return {"condition": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditionCount():
    """Fetch the total count of termination conditions.
    
    Returns:
        dict: A dictionary containing the termination condition count.
    """
    try:
        result = contract.functions.getTerminationConditionCount().call()
        return {"count": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def createObligation(party, description, penaltyForBreach):
    """Create a new obligation.
    
    Args:
        party (string): The party responsible for the obligation.
        description (string): The description of the obligation.
        penaltyForBreach (string): The penalty for breaching this obligation.
        
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.createObligation(party, description, penaltyForBreach).buildTransaction({
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
def addSpecialTerm(term):
    """Add a special term to the NDA.
    
    Args:
        term (string): The special term to add.
        
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.addSpecialTerm(term).buildTransaction({
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
def addTerminationCondition(condition):
    """Add a termination condition to the NDA.
    
    Args:
        condition (string): The condition to add.
        
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.addTerminationCondition(condition).buildTransaction({
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