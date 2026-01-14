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
def checkObligation():
    """Call checkObligation on the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: checkObligation", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: checkObligation\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        txn = contract.functions.checkObligation().buildTransaction({
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
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
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
        sys.stderr.write(f"[MCP] Tool called: makePayment\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        txn = contract.functions.makePayment(amount).buildTransaction({
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
        print("[MCP] Returning transaction hash", flush=True)
        return {"tx_hash": tx_hash.hex()}
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
    print("[MCP] Tool called: getBorrower", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getBorrower\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getBorrower().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getBorrowerObligation():
    """Get getBorrowerObligation from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getBorrowerObligation", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getBorrowerObligation\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getBorrowerObligation().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getBorrowerObligationPenalty():
    """Get getBorrowerObligationPenalty from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getBorrowerObligationPenalty", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getBorrowerObligationPenalty\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getBorrowerObligationPenalty().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getDisbursementDate():
    """Get getDisbursementDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getDisbursementDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getDisbursementDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getDisbursementDate().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getFirstPaymentDueDate():
    """Get getFirstPaymentDueDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getFirstPaymentDueDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getFirstPaymentDueDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getFirstPaymentDueDate().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getLoanAmount():
    """Get getLoanAmount from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getLoanAmount", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getLoanAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getLoanAmount().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getLender():
    """Get getLender from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getLender", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getLender\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getLender().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getMonthlyPaymentAmount():
    """Get getMonthlyPaymentAmount from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getMonthlyPaymentAmount", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getMonthlyPaymentAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getMonthlyPaymentAmount().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getOriginationFeeAmount():
    """Get getOriginationFeeAmount from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getOriginationFeeAmount", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getOriginationFeeAmount\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getOriginationFeeAmount().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getStartDate():
    """Get getStartDate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getStartDate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getStartDate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getStartDate().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def getDefaultInterestRate():
    """Get getDefaultInterestRate from the contract.
    
    Returns: Contract data
    """
    print("[MCP] Tool called: getDefaultInterestRate", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: getDefaultInterestRate\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        print("[MCP] Calling contract function...", flush=True)
        result = contract.functions.getDefaultInterestRate().call()
        sys.stderr.write(f"[MCP] Returning result: {str(type(result).__name__)}\n")
        sys.stderr.flush()
        print("[MCP] Returning result: " + str(type(result).__name__), flush=True)
        return {"result": result}
    except Exception as e:
        error_msg = str(e)
        sys.stderr.write(f"[MCP] Error: {error_msg}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        return {"error": error_msg}

@mcp.tool()
def initializeAgreement(_lender, _borrower, _loanAmount, _monthlyPayment, _originationFee, _startDate, _disbursementDate, _firstPaymentDueDate, _borrowerObligation, _borrowerObligationPenalty, _defaultInterestRate, _defaultAcceleration):
    """Call initializeAgreement on the contract.
    
    Args:
          _lender: address - _lender
          _borrower: address - _borrower
          _loanAmount: uint256 - _loanAmount
          _monthlyPayment: uint256 - _monthlyPayment
          _originationFee: uint256 - _originationFee
          _startDate: uint256 - _startDate
          _disbursementDate: uint256 - _disbursementDate
          _firstPaymentDueDate: uint256 - _firstPaymentDueDate
          _borrowerObligation: string - _borrowerObligation
          _borrowerObligationPenalty: string - _borrowerObligationPenalty
          _defaultInterestRate: uint256 - _defaultInterestRate
          _defaultAcceleration: string - _defaultAcceleration
    """
    print("[MCP] Tool called: initializeAgreement", flush=True)
    print("[MCP] Attempting execution...", flush=True)
    try:
        sys.stderr.write(f"[MCP] Tool called: initializeAgreement\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Attempting execution...\n")
        sys.stderr.flush()
        sys.stderr.write(f"[MCP] Calling contract function...\n")
        sys.stderr.flush()
        txn = contract.functions.initializeAgreement(_lender, _borrower, _loanAmount, _monthlyPayment, _originationFee, _startDate, _disbursementDate, _firstPaymentDueDate, _borrowerObligation, _borrowerObligationPenalty, _defaultInterestRate, _defaultAcceleration).buildTransaction({
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
        print("[MCP] Returning transaction hash", flush=True)
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
    print("[MCP] Attempting execution...", flush=True)
    try:
        mcp.run()
    except Exception as e:
        sys.stderr.write(f"[MCP] Runtime error: {{e}}\n")
        sys.stderr.flush()
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)
