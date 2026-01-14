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
abi_path = Path(__file__).parent / 'TechCorp_I_Robert_Joh.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("TechCorp_I_Robert_Joh")

@mcp.tool()
def terminateEmployment():
    """Terminate the employment agreement.
    Only the employer can call this function.
    Returns the transaction hash of the termination transaction.
    """
    try:
        txn = contract.functions.terminateEmployment().buildTransaction({
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
def payCompensation():
    """Pay compensation to the employee.
    Only the employer can call this function.
    Returns the transaction hash of the compensation payment transaction.
    """
    try:
        txn = contract.functions.payCompensation().buildTransaction({
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
def getFinancialTerms():
    """Get the financial terms of the employment agreement.
    Returns an array of financial terms.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligations():
    """Get the obligations of the employer and employee.
    Returns an array of obligations.
    """
    try:
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """Get the special terms of the employment agreement.
    Returns an array of special terms.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employer():
    """Get the address of the employer.
    Returns the employer's address.
    """
    try:
        result = contract.functions.employer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employee():
    """Get the address of the employee.
    Returns the employee's address.
    """
    try:
        result = contract.functions.employee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def status():
    """Get the current status of the employment agreement.
    Returns the status as an integer (uint8).
    """
    try:
        result = contract.functions.status().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()