#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

print("[MCP] Starting server initialization...", flush=True)

try:
    from web3 import Web3
    from dotenv import load_dotenv
    from fastmcp import FastMCP
    print("[MCP] Imports successful", flush=True)
except Exception as e:
    print(f"[MCP] Import error: {e}", flush=True)
    sys.exit(1)

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
print(f"[MCP] Loading env from: {env_path}", flush=True)
load_dotenv(dotenv_path=env_path)

# Load ABI from the same directory as this script
abi_path = Path(__file__).parent / 'loan.abi.json'
print(f"[MCP] Loading ABI from: {abi_path}", flush=True)
try:
    with open(abi_path, 'r') as f:
        contract_abi = json.load(f)
    print(f"[MCP] ABI loaded successfully ({len(contract_abi)} items)", flush=True)
except Exception as e:
    print(f"[MCP] ABI load error: {e}", flush=True)
    sys.exit(1)

# Get environment variables
RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')

print(f"[MCP] RPC_URL: {RPC_URL}", flush=True)
print(f"[MCP] CONTRACT_ADDRESS: {CONTRACT_ADDRESS}", flush=True)
print(f"[MCP] ACCOUNT_ADDRESS: {ACCOUNT_ADDRESS}", flush=True)

# Initialize Web3
try:
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    print(f"[MCP] Web3 connected: {web3.is_connected()}", flush=True)
except Exception as e:
    print(f"[MCP] Web3 connection error: {e}", flush=True)
    sys.exit(1)

# Set up account and contract
try:
    account_address = Web3.to_checksum_address(ACCOUNT_ADDRESS)
    contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
    print(f"[MCP] Contract initialized successfully", flush=True)
except Exception as e:
    print(f"[MCP] Contract setup error: {e}", flush=True)
    sys.exit(1)

# Create FastMCP instance
mcp = FastMCP("loan")
print("[MCP] FastMCP instance created", flush=True)

@mcp.tool()
def getLender():
    """Get getLender from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getLender", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getLender", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getLender().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
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
        print("[MCP] Tool called: getBorrower", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getBorrower().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getLoanDetails():
    """Get getLoanDetails from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getLoanDetails", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getLoanDetails", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getLoanDetails().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getMonthlyPaymentDetails():
    """Get getMonthlyPaymentDetails from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getMonthlyPaymentDetails", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getMonthlyPaymentDetails", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getMonthlyPaymentDetails().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getOriginationFeeDetails():
    """Get getOriginationFeeDetails from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getOriginationFeeDetails", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getOriginationFeeDetails", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getOriginationFeeDetails().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getExecutionDate():
    """Get getExecutionDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getExecutionDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getExecutionDate", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getExecutionDate().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getDisbursementDate():
    """Get getDisbursementDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getDisbursementDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getDisbursementDate", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getDisbursementDate().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getFirstPaymentDueDate():
    """Get getFirstPaymentDueDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getFirstPaymentDueDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getFirstPaymentDueDate", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getFirstPaymentDueDate().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getObligationCount():
    """Get getObligationCount from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getObligationCount", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getObligationCount", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getObligationCount().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
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
        print("[MCP] Tool called: getObligation", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getObligation(index).call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getSpecialTerms():
    """Get getSpecialTerms from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getSpecialTerms", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getSpecialTerms", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getSpecialTerms().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def getTerminationConditions():
    """Get getTerminationConditions from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getTerminationConditions", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: getTerminationConditions", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getTerminationConditions().call()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def performLoanDisbursement():
    """Call performLoanDisbursement on the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: performLoanDisbursement", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: performLoanDisbursement", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        txn = contract.functions.performLoanDisbursement().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        print("[MCP] Sending transaction...", flush=True)
        tx_hash = web3.eth.send_transaction(txn)
        print("[MCP] Returning transaction hash", flush=True)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}

@mcp.tool()
def makePayment(amount):
    """Call makePayment on the contract.
    
    Args:
          amount: uint256 - amount
    """
    print("[MCP] Tool called: makePayment", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        print("[MCP] Tool called: makePayment", flush=True)
        print("[MCP] Attempting execution...", flush=True)
        print("[MCP] Calling contract function...", flush=True)
        txn = contract.functions.makePayment(amount).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        print("[MCP] Sending transaction...", flush=True)
        tx_hash = web3.eth.send_transaction(txn)
        print("[MCP] Returning transaction hash", flush=True)
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        print("[MCP] Error: " + error_msg, flush=True)
        import traceback
        traceback.print_exc()
        return {"error": error_msg}


if __name__ == "__main__":
    print("[MCP] Starting mcp.run()...", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        mcp.run()
    except Exception as e:
        print(f"[MCP] Runtime error: {{e}}", flush=True)
        import traceback
        traceback.print_exc()
        sys.exit(1)
