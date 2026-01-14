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

# Load ABI
abi_path = Path(__file__).parent / 'loan.abi.json'
sys.stderr.write(f"[MCP] Loading ABI from: {abi_path}\n")
sys.stderr.flush()
try:
    with open(abi_path, 'r') as f:
        contract_abi = json.load(f)
    sys.stderr.write(f"[MCP] ABI loaded ({len(contract_abi)} items)\n")
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

# Initialize Web3 with timeout
try:
    web3 = Web3(Web3.HTTPProvider(RPC_URL, request_kwargs={'timeout': 10}))
    
    # Test connection immediately
    if not web3.is_connected():
        sys.stderr.write(f"[MCP] ERROR: Cannot connect to RPC at {RPC_URL}\n")
        sys.stderr.flush()
        sys.exit(1)
    
    sys.stderr.write(f"[MCP] Web3 connected successfully\n")
    sys.stderr.flush()
    
    # Test if we can get latest block (verifies RPC is working)
    try:
        latest_block = web3.eth.block_number
        sys.stderr.write(f"[MCP] Latest block: {latest_block}\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[MCP] WARNING: Cannot get latest block: {e}\n")
        sys.stderr.flush()
    
except Exception as e:
    sys.stderr.write(f"[MCP] Web3 connection error: {e}\n")
    sys.stderr.flush()
    sys.exit(1)

# Set up account and contract
try:
    account_address = Web3.to_checksum_address(ACCOUNT_ADDRESS)
    contract_address_checksum = Web3.to_checksum_address(CONTRACT_ADDRESS)
    
    # Verify contract exists
    try:
        code = web3.eth.get_code(contract_address_checksum)
        if code == b'' or code == '0x':
            sys.stderr.write(f"[MCP] ERROR: No contract code at address {contract_address_checksum}\n")
            sys.stderr.flush()
            sys.exit(1)
        sys.stderr.write(f"[MCP] Contract code verified ({len(code)} bytes)\n")
        sys.stderr.flush()
    except Exception as e:
        sys.stderr.write(f"[MCP] ERROR checking contract code: {e}\n")
        sys.stderr.flush()
        sys.exit(1)
    
    contract = web3.eth.contract(address=contract_address_checksum, abi=contract_abi)
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
def getBorrower():
    """Get getBorrower from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getBorrower\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getBorrower().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getBorrowerObligation():
    """Get getBorrowerObligation from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getBorrowerObligation\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getBorrowerObligation().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getDefaultInterestRate():
    """Get getDefaultInterestRate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getDefaultInterestRate\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getDefaultInterestRate().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getDefaultTriggers():
    """Get getDefaultTriggers from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getDefaultTriggers\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getDefaultTriggers().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getDisbursementDate():
    """Get getDisbursementDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getDisbursementDate\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getDisbursementDate().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getFirstPaymentDate():
    """Get getFirstPaymentDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getFirstPaymentDate\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getFirstPaymentDate().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getLender():
    """Get getLender from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getLender\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getLender().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getLatePaymentFee():
    """Get getLatePaymentFee from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getLatePaymentFee\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getLatePaymentFee().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getLoanAmount():
    """Get getLoanAmount from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getLoanAmount\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getLoanAmount().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getLoanStartDate():
    """Get getLoanStartDate from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getLoanStartDate\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getLoanStartDate().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getMonthlyPayment():
    """Get getMonthlyPayment from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getMonthlyPayment\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getMonthlyPayment().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def getAccelerationTerm():
    """Get getAccelerationTerm from the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling view function getAccelerationTerm\n")
        sys.stderr.flush()
        
        # CRITICAL FIX: Add explicit timeout and error handling
        try:
            # Create a call with explicit timeout
            result = contract.functions.getAccelerationTerm().call(block_identifier='latest')
            
            sys.stderr.write(f"[MCP] Result: {result}\n")
            sys.stderr.flush()
            
            # Handle different return types
            if isinstance(result, bytes):
                result = result.hex()
            elif isinstance(result, tuple):
                result = list(result)
            
            return {"result": result}
            
        except Exception as call_error:
            error_msg = str(call_error)
            sys.stderr.write(f"[MCP] Contract call failed: {error_msg}\n")
            sys.stderr.flush()
            
            # Try to diagnose the issue
            if "execution reverted" in error_msg.lower():
                return {"error": "Contract execution reverted. The function may require different parameters or the contract state doesn't allow this call."}
            elif "invalid opcode" in error_msg.lower():
                return {"error": "Invalid contract bytecode. The contract may not be deployed correctly."}
            elif "timeout" in error_msg.lower():
                return {"error": "RPC timeout. Check your Ganache connection."}
            else:
                return {"error": f"Contract call failed: {error_msg}"}
        
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] EXCEPTION: {error_msg}\n")
        sys.stderr.flush()
        return {"error": error_msg}

@mcp.tool()
def makePayment(amount):
    """Call makePayment on the contract.
    
    Args:
          amount: uint256
    """
    try:
        sys.stderr.write(f"[MCP] Calling makePayment\n")
        sys.stderr.flush()
        
        # Get nonce with timeout
        try:
            nonce = web3.eth.get_transaction_count(account_address, timeout=5)
        except Exception as e:
            return {"error": f"Failed to get nonce: {str(e)}"}
        
        # Build transaction with timeout
        try:
            txn = contract.functions.makePayment(amount).build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.eth.gas_price
            })
        except Exception as e:
            return {"error": f"Failed to build transaction: {str(e)}"}
        
        # Send transaction
        try:
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Transaction sent: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return {"tx_hash": tx_hash.hex()}
        except Exception as e:
            return {"error": f"Transaction failed: {str(e)}"}
            
    except Exception as e:
        sys.stderr.write(f"[MCP] ERROR: {str(e)}\n")
        sys.stderr.flush()
        return {"error": str(e)}

@mcp.tool()
def fulfillObligation():
    """Call fulfillObligation on the contract.
    
    Returns: Contract data
    """
    try:
        sys.stderr.write(f"[MCP] Calling fulfillObligation\n")
        sys.stderr.flush()
        
        # Get nonce with timeout
        try:
            nonce = web3.eth.get_transaction_count(account_address, timeout=5)
        except Exception as e:
            return {"error": f"Failed to get nonce: {str(e)}"}
        
        # Build transaction with timeout
        try:
            txn = contract.functions.fulfillObligation().build_transaction({
                'from': account_address,
                'nonce': nonce,
                'gas': 2000000,
                'gasPrice': web3.eth.gas_price
            })
        except Exception as e:
            return {"error": f"Failed to build transaction: {str(e)}"}
        
        # Send transaction
        try:
            tx_hash = web3.eth.send_transaction(txn)
            sys.stderr.write(f"[MCP] Transaction sent: {tx_hash.hex()}\n")
            sys.stderr.flush()
            return {"tx_hash": tx_hash.hex()}
        except Exception as e:
            return {"error": f"Transaction failed: {str(e)}"}
            
    except Exception as e:
        sys.stderr.write(f"[MCP] ERROR: {str(e)}\n")
        sys.stderr.flush()
        return {"error": str(e)}


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
