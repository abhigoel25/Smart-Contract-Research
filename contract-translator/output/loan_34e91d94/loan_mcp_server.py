#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path

sys.stderr.write("[MCP] Starting server initialization...\n")
sys.stderr.flush()

try:
    from web3 import Web3
    from dotenv import load_dotenv
    from fastmcp import FastMCP
    sys.stderr.write("[MCP] Imports successful\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] Import error: {e}\n")
    sys.stderr.flush()
    sys.exit(1)

# Load .env from the same directory as this script
env_path = Path(__file__).parent / '.env'
sys.stderr.write(f"[MCP] Loading env from: {env_path}\n")
sys.stderr.flush()
load_dotenv(dotenv_path=env_path)

# Load ABI from the same directory as this script
abi_path = Path(__file__).parent / 'loan.abi.json'
sys.stderr.write(f"[MCP] Loading ABI from: {abi_path}\n")
sys.stderr.flush()
try:
    with open(abi_path, 'r') as f:
        contract_abi = json.load(f)
    sys.stderr.write(f"[MCP] ABI loaded successfully ({len(contract_abi)} items)\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] ABI load error: {e}\n")
    sys.stderr.flush()
    sys.exit(1)

# Get environment variables
RPC_URL = os.getenv('RPC_URL')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')

sys.stderr.write(f"[MCP] RPC_URL: {RPC_URL}\n")
sys.stderr.flush()
sys.stderr.write(f"[MCP] CONTRACT_ADDRESS: {CONTRACT_ADDRESS}\n")
sys.stderr.flush()
sys.stderr.write(f"[MCP] ACCOUNT_ADDRESS: {ACCOUNT_ADDRESS}\n")
sys.stderr.flush()

# Initialize Web3
try:
    web3 = Web3(Web3.HTTPProvider(RPC_URL))
    sys.stderr.write(f"[MCP] Web3 connected: {web3.is_connected()}\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] Web3 connection error: {e}\n")
    sys.stderr.flush()
    sys.exit(1)

# Set up account and contract
try:
    account_address = Web3.to_checksum_address(ACCOUNT_ADDRESS)
    contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)
    sys.stderr.write(f"[MCP] Contract initialized successfully\n")
    sys.stderr.flush()
except Exception as e:
    sys.stderr.write(f"[MCP] Contract setup error: {e}\n")
    sys.stderr.flush()
    sys.exit(1)

# Create FastMCP instance
mcp = FastMCP("loan")
sys.stderr.write("[MCP] FastMCP instance created\n")
sys.stderr.flush()

@mcp.tool()
def getLender():
    """Get getLender from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getLender\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        result = contract.functions.getLender().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getBorrower():
    """Get getBorrower from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getBorrower\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        result = contract.functions.getBorrower().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getFinancialTerm(index):
    """Get getFinancialTerm from the contract.
    
    Args:
          index: uint256 - index
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getFinancialTerm\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        result = contract.functions.getFinancialTerm(index).call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getDate(index):
    """Get getDate from the contract.
    
    Args:
          index: uint256 - index
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        result = contract.functions.getDate(index).call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getObligation(index):
    """Get getObligation from the contract.
    
    Args:
          index: uint256 - index
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getObligation\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        result = contract.functions.getObligation(index).call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def acknowledgeObligation(index):
    """Call acknowledgeObligation on the contract.
    
    Args:
          index: uint256 - index
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: acknowledgeObligation\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        txn = contract.functions.acknowledgeObligation(index).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        sys.stderr.write(f"[MCP] Sending transaction...\n")
        sys.stderr.flush()
        tx_hash = web3.eth.send_transaction(txn)
        sys.stderr.write(f"[MCP] Returning transaction hash\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def makePayment(paymentAmount):
    """Call makePayment on the contract.
    
    Args:
          paymentAmount: uint256 - paymentAmount
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: makePayment\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        txn = contract.functions.makePayment(paymentAmount).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        sys.stderr.write(f"[MCP] Sending transaction...\n")
        sys.stderr.flush()
        tx_hash = web3.eth.send_transaction(txn)
        sys.stderr.write(f"[MCP] Returning transaction hash\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}


if __name__ == "__main__":
    sys.stderr.write("[MCP] Starting mcp.run()...\n")
    sys.stderr.flush()
    try:
        mcp.run()
    except Exception as e:
        sys.stderr.write(f"[MCP] Runtime error: {{e}}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
