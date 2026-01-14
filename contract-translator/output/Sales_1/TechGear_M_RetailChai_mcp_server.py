import os
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env in the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Set up Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)

# Contract ABI
ABI = [
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_buyer",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [],
        "name": "fulfillObligation",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
        "payable": false
    },
    {
        "inputs": [],
        "name": "getFinancialTerms",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint256",
                        "name": "amount",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "currency",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "purpose",
                        "type": "string"
                    },
                    {
                        "internalType": "bool",
                        "name": "isPaid",
                        "type": "bool"
                    }
                ],
                "internalType": "struct SalesAgreement.FinancialTerm[3]",
                "name": "",
                "type": "tuple[3]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getObligations",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "string",
                        "name": "description",
                        "type": "string"
                    },
                    {
                        "internalType": "string",
                        "name": "deadline",
                        "type": "string"
                    },
                    {
                        "internalType": "bool",
                        "name": "isFulfilled",
                        "type": "bool"
                    }
                ],
                "internalType": "struct SalesAgreement.Obligation[2]",
                "name": "",
                "type": "tuple[2]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "payDownPayment",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "confirmProductionCompletion",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "finalizeDelivery",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "string",
                "name": "reason",
                "type": "string"
            }
        ],
        "name": "terminateAgreement",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "paymentStatus",
        "outputs": [
            {
                "internalType": "enum SalesAgreement.PaymentStatus",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "seller",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "buyer",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# Create FastMCP instance
mcp = FastMCP("TechGear_M_RetailChai")

@mcp.tool()
def fulfillObligation():
    """Fulfill the obligation in the sales agreement.
    Can be called by the seller.
    
    Returns:
        dict: Transaction hash
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        txn = contract.functions.fulfillObligation().buildTransaction({
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
    """Get the financial terms of the sales agreement.
    
    Returns:
        dict: Financial terms
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@Mcp.tool()
def getObligations():
    """Get obligations related to the sales agreement.
    
    Returns:
        dict: List of obligations
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        result = contract.functions.getObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@Mcp.tool()
def payDownPayment():
    """Pay the down payment as specified in the sales agreement.
    Can be called by the buyer.
    
    Returns:
        dict: Transaction hash
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        txn = contract.functions.payDownPayment().buildTransaction({
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
def confirmProductionCompletion():
    """Confirm that production has been completed.
    Can be called by the seller.
    
    Returns:
        dict: Transaction hash
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        txn = contract.functions.confirmProductionCompletion().buildTransaction({
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
def finalizeDelivery():
    """Finalize the delivery of goods in accordance with the sales agreement.
    Can be called by the seller.
    
    Returns:
        dict: Transaction hash
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        txn = contract.functions.finalizeDelivery().buildTransaction({
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
def terminateAgreement(reason: str):
    """Terminate the sales agreement.
    Can be called by either party.
    
    Args:
        reason (str): Reason for termination.
        
    Returns:
        dict: Transaction hash
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        txn = contract.functions.terminateAgreement(reason).buildTransaction({
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
def paymentStatus():
    """Get the current payment status of the sales agreement.
    
    Returns:
        dict: Payment status
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        result = contract.functions.paymentStatus().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def seller():
    """Get the address of the seller.
    
    Returns:
        dict: Seller address
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        result = contract.functions.seller().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def buyer():
    """Get the address of the buyer.
    
    Returns:
        dict: Buyer address
    """
    try:
        contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)
        result = contract.functions.buyer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()