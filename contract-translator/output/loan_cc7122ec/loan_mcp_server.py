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
abi_path = Path(__file__).parent / 'loan.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("Capital_Fi_GreenTech_")

@mcp.tool()
def getLender():
    """Get the lender information.

    Returns:
        dict: Contains lender details.
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
    """Get the borrower information.

    Returns:
        dict: Contains borrower details.
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
def getFinancialTerm(index: int):
    """Get financial term details by index.

    Args:
        index (int): The index of the financial term.

    Returns:
        dict: Contains financial term details.
    """
    print("[MCP] Tool called: getFinancialTerm", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getFinancialTerm(index).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getImportantDate(index: int):
    """Get important date details by index.

    Args:
        index (int): The index of the important date.

    Returns:
        dict: Contains important date details.
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
def getObligation(index: int):
    """Get obligation details by index.

    Args:
        index (int): The index of the obligation.

    Returns:
        dict: Contains obligation details.
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
def maintainInsuranceOnCollateral():
    """Maintain insurance on collateral (non-payable).

    Returns:
        dict: Contains transaction hash.
    """
    print("[MCP] Tool called: maintainInsuranceOnCollateral", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        txn = contract.functions.maintainInsuranceOnCollateral().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def holdFirstSecurityInterest():
    """Hold the first security interest (non-payable).

    Returns:
        dict: Contains transaction hash.
    """
    print("[MCP] Tool called: holdFirstSecurityInterest", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        txn = contract.functions.holdFirstSecurityInterest().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def prepayLoan(amount: int):
    """Prepay the loan with a specified amount (non-payable).

    Args:
        amount (int): The amount to be prepaid in wei.

    Returns:
        dict: Contains transaction hash.
    """
    print("[MCP] Tool called: prepayLoan", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        txn = contract.functions.prepayLoan(amount).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

if __name__ == "__main__":
    mcp.run()