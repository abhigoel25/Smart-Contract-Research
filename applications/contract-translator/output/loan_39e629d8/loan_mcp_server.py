import os
import json
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load ABI from the same directory as this script
abi_path = Path(__file__).parent / 'loan.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("loan")

@mcp.tool()
def getLender():
    """Get getLender from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getLender", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getLender().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getBorrower():
    """Get getBorrower from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getBorrower", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getBorrower().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getFinancialTerms(index):
    """Get getFinancialTerms from the contract.
    
    Args:
          index: uint256 - index
    """
    print("[MCP] Tool called: getFinancialTerms", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getFinancialTerms(index).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getImportantDate(index):
    """Get getImportantDate from the contract.
    
    Args:
          index: uint256 - index
    """
    print("[MCP] Tool called: getImportantDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getImportantDate(index).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getObligation(index):
    """Get getObligation from the contract.
    
    Args:
          index: uint256 - index
    """
    print("[MCP] Tool called: getObligation", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getObligation(index).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def fulfillObligation(index):
    """Call fulfillObligation on the contract.
    
    Args:
          index: uint256 - index
    """
    print("[MCP] Tool called: fulfillObligation", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.fulfillObligation(index).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(result)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def checkLoanAmount():
    """Get checkLoanAmount from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: checkLoanAmount", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.checkLoanAmount().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def calculateDefaultInterest(unpaidAmount):
    """Get calculateDefaultInterest from the contract.
    
    Args:
          unpaidAmount: uint256 - unpaidAmount
    """
    print("[MCP] Tool called: calculateDefaultInterest", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.calculateDefaultInterest(unpaidAmount).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}


if __name__ == "__main__":
    mcp.run()
