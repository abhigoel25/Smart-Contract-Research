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

# Create FastMCP instance
mcp = FastMCP("TechGear_M_RetailChai")

@mcp.tool()
def canTerminate():
    """Check if the agreement can be terminated.
    
    Returns:
        bool: True if the agreement can be terminated, False otherwise.
    """
    try:
        result = contract.functions.canTerminate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def deliveryDeadline():
    """Get the delivery deadline.
    
    Returns:
        uint256: Delivery deadline as a timestamp.
    """
    try:
        result = contract.functions.deliveryDeadline().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def deliverGoods(item: str, quantity: int):
    """Deliver goods to the buyer.
    
    Args:
        item (str): The item to be delivered.
        quantity (int): The quantity of the item.
    
    Returns:
        dict: Transaction hash of the delivery.
    """
    try:
        txn = contract.functions.deliverGoods(item, quantity).buildTransaction({
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
def downPaymentAmount():
    """Get the down payment amount.
    
    Returns:
        uint256: Down payment amount.
    """
    try:
        result = contract.functions.downPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def effectivedate():
    """Get the effective date of the agreement.
    
    Returns:
        uint256: Effective date as a timestamp.
    """
    try:
        result = contract.functions.effectivedate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def finalPaymentAmount():
    """Get the final payment amount.
    
    Returns:
        uint256: Final payment amount.
    """
    try:
        result = contract.functions.finalPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def paymentStage():
    """Get the current payment stage.
    
    Returns:
        uint8: Current payment stage.
    """
    try:
        result = contract.functions.paymentStage().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payUponDeliveryInspection():
    """Make payment upon delivery inspection.
    
    Returns:
        dict: Transaction hash of the payment.
    """
    try:
        txn = contract.functions.payUponDeliveryInspection().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(5, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def payUponProductionCompletion():
    """Make payment upon production completion.
    
    Returns:
        dict: Transaction hash of the payment.
    """
    try:
        txn = contract.functions.payUponProductionCompletion().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(10, 'ether')  # Example amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def seller():
    """Get the seller's address.
    
    Returns:
        address: Seller's Ethereum address.
    """
    try:
        result = contract.functions.seller().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def totalValue():
    """Get the total value of the agreement.
    
    Returns:
        uint256: Total value.
    """
    try:
        result = contract.functions.totalValue().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def productionPaymentAmount():
    """Get the production payment amount.
    
    Returns:
        uint256: Production payment amount.
    """
    try:
        result = contract.functions.productionPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def terminateAgreement():
    """Terminate the agreement.
    
    Returns:
        dict: Transaction hash of the termination.
    """
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
def deliveryDate():
    """Get the delivery date.
    
    Returns:
        uint256: Delivery date as a timestamp.
    """
    try:
        result = contract.functions.deliveryDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()