#!/usr/bin/env python3
import os
import json
import sys
from pathlib import Path
from threading import Thread
import time

sys.stderr.write("[MCP] Starting server initialization...\n")
sys.stderr.flush()

# Helper function to execute with timeout
def call_with_timeout(func, timeout=10):
    """Execute a function with a timeout (threading-based for Windows compatibility)"""
    result = {}
    error = {}
    
    def target():
        try:
            result['value'] = func()
        except Exception as e:
            error['value'] = e
    
    thread = Thread(target=target, daemon=False)
    thread.start()
    thread.join(timeout=timeout)
    
    if thread.is_alive():
        raise TimeoutError(f"Function call exceeded {timeout} second timeout")
    
    if error:
        raise error['value']
    
    return result.get('value')


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
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getLender...\n")
            sys.stderr.flush()
            result = contract.functions.getLender().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
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
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getBorrower...\n")
            sys.stderr.flush()
            result = contract.functions.getBorrower().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getLoanAmount():
    """Get getLoanAmount from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getLoanAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getLoanAmount...\n")
            sys.stderr.flush()
            result = contract.functions.getLoanAmount().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getMonthlyPaymentAmount():
    """Get getMonthlyPaymentAmount from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getMonthlyPaymentAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getMonthlyPaymentAmount...\n")
            sys.stderr.flush()
            result = contract.functions.getMonthlyPaymentAmount().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getOriginationFeeAmount():
    """Get getOriginationFeeAmount from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getOriginationFeeAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getOriginationFeeAmount...\n")
            sys.stderr.flush()
            result = contract.functions.getOriginationFeeAmount().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getStartDate():
    """Get getStartDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getStartDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getStartDate...\n")
            sys.stderr.flush()
            result = contract.functions.getStartDate().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getDisbursementDate():
    """Get getDisbursementDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getDisbursementDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getDisbursementDate...\n")
            sys.stderr.flush()
            result = contract.functions.getDisbursementDate().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getFirstPaymentDueDate():
    """Get getFirstPaymentDueDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getFirstPaymentDueDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getFirstPaymentDueDate...\n")
            sys.stderr.flush()
            result = contract.functions.getFirstPaymentDueDate().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getTermEndDate():
    """Get getTermEndDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getTermEndDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getTermEndDate...\n")
            sys.stderr.flush()
            result = contract.functions.getTermEndDate().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def maintainInsurance():
    """Call maintainInsurance on the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: maintainInsurance\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.maintainInsurance().buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def prepayLoan():
    """Call prepayLoan on the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: prepayLoan\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.prepayLoan().buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def setDefaultConditions(triggers, acceleration, interestRate):
    """Call setDefaultConditions on the contract.
    
    Args:
          triggers: string - triggers
          acceleration: string - acceleration
          interestRate: string - interestRate
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: setDefaultConditions\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.setDefaultConditions(triggers, acceleration, interestRate).buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getDefaultConditions():
    """Get getDefaultConditions from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: getDefaultConditions\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Creating function reference...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def make_call():
            sys.stderr.write(f"[MCP] Inside timeout wrapper, about to call contract.functions.getDefaultConditions...\n")
            sys.stderr.flush()
            result = contract.functions.getDefaultConditions().call()
            sys.stderr.write(f"[MCP] Contract call returned, result type: {type(result).__name__}\n")
            sys.stderr.flush()
            return result
        
        sys.stderr.write(f"[MCP] Starting timeout wrapper with 10s limit...\n")
        sys.stderr.flush()
        result = call_with_timeout(make_call, timeout=10)
        
        sys.stderr.write(f"[MCP] Timeout wrapper succeeded, result: {result}\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Returning result to MCP client\n")
        sys.stderr.flush()
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in tool: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def setDisbursementDate(_disbursementDate):
    """Call setDisbursementDate on the contract.
    
    Args:
          _disbursementDate: uint256 - _disbursementDate
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: setDisbursementDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.setDisbursementDate(_disbursementDate).buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def setFirstPaymentDueDate(_firstPaymentDueDate):
    """Call setFirstPaymentDueDate on the contract.
    
    Args:
          _firstPaymentDueDate: uint256 - _firstPaymentDueDate
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: setFirstPaymentDueDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.setFirstPaymentDueDate(_firstPaymentDueDate).buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def setTermEndDate(_termEndDate):
    """Call setTermEndDate on the contract.
    
    Args:
          _termEndDate: uint256 - _termEndDate
    """
    try:
        sys.stderr.write(f"[MCP] Tool called: setTermEndDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Preparing transaction build...\n")
        sys.stderr.flush()
        
        # Use timeout wrapper to prevent hanging
        def build_transaction():
            sys.stderr.write(f"[MCP] Inside timeout: Getting nonce...\n")
            sys.stderr.flush()
            nonce = web3.eth.get_transaction_count(account_address)
            sys.stderr.write(f"[MCP] Inside timeout: Got nonce {nonce}, building transaction...\n")
            sys.stderr.flush()
            return contract.functions.setTermEndDate(_termEndDate).buildTransaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.to_wei('20', 'gwei')
            })
        
        sys.stderr.write(f"[MCP] Starting buildTransaction with 10s timeout...\n")
        sys.stderr.flush()
        txn = call_with_timeout(build_transaction, timeout=10)
        
        sys.stderr.write(f"[MCP] Transaction built, now sending...\n")
        sys.stderr.flush()
        
        def send_tx():
            sys.stderr.write(f"[MCP] Inside timeout: Sending transaction...\n")
            sys.stderr.flush()
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Inside timeout: Transaction sent, hash: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return tx_hash
        
        sys.stderr.write(f"[MCP] Starting send_transaction with 15s timeout...\n")
        sys.stderr.flush()
        tx_hash = call_with_timeout(send_tx, timeout=15)
        
        sys.stderr.write(f"[MCP] Transaction successful: {tx_hash.hex()}\n")
        sys.stderr.flush()
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION in transaction: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.stderr.flush()
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
