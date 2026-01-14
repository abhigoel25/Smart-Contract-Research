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
abi_path = Path(__file__).parent / 'TechGear_M_RetailChai.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("TechGear_M_RetailChai")

@mcp.tool()
def confirmDelivery():
    """Confirms the delivery of goods. Can only be called by the seller."""
    try:
        txn = contract.functions.confirmDelivery().buildTransaction({
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
def terminateAgreement():
    """Terminates the agreement. Can only be called by the seller or buyer."""
    try:
        txn = contract.functions.terminateAgreement().buildTransaction({
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
def deliveryCost():
    """Returns the delivery cost. View function, no parameters."""
    try:
        result = contract.functions.deliveryCost().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def downPayment():
    """Returns the down payment amount. View function, no parameters."""
    try:
        result = contract.functions.downPayment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def isAgreementActive():
    """Checks if the agreement is currently active. View function, no parameters."""
    try:
        result = contract.functions.isAgreementActive().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payment1():
    """Returns the first payment amount. View function, no parameters."""
    try:
        result = contract.functions.payment1().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payment2():
    """Returns the second payment amount. View function, no parameters."""
    try:
        result = contract.functions.payment2().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def seller():
    """Returns the seller's address. View function, no parameters."""
    try:
        result = contract.functions.seller().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def state():
    """Returns the current state of the agreement. View function, no parameters."""
    try:
        result = contract.functions.state().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def totalPurchasePrice():
    """Returns the total purchase price. View function, no parameters."""
    try:
        result = contract.functions.totalPurchasePrice().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def buyer():
    """Returns the buyer's address. View function, no parameters."""
    try:
        result = contract.functions.buyer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def obligations(obligation_id: str):
    """Returns the obligations for a given obligation ID. Requires the obligation ID string."""
    try:
        result = contract.functions.obligations(obligation_id).call()
        return {"party": result[0], "description": result[1], "deadline": result[2], "penaltyForBreach": result[3]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def agreementDate():
    """Returns the agreement date. View function, no parameters."""
    try:
        result = contract.functions.agreementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()