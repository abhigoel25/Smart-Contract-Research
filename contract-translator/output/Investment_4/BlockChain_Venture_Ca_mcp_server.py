import os
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables from .env in the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_investor",
                "type": "address"
            }
        ],
        "name": "setInvestor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "makeInvestment",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_timestamp",
                "type": "uint256"
            }
        ],
        "name": "setRedemptionEvent",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "redeemShares",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "distributeDividends",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "grantBoardSeat",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getStatus",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "company",
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
        "name": "investor",
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
        "name": "PURCHASE_PRICE_PER_SHARE",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "TOTAL_INVESTMENT_AMOUNT",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "investmentTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "redemptionEventTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "sharesRedeemed",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)
mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def setInvestor(_investor: str):
    """Set the investor address.
    
    Requires the investor address as a parameter.
    Can only be called by the contract owner.
    
    Args:
        _investor (str): The address of the investor.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.setInvestor(_investor).buildTransaction({
            'chainId': 1,  # Update to your desired chain ID
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(web3.eth.defaultAccount),
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makeInvestment():
    """Make an investment in the smart contract.

    This function is payable and requires the amount to be transferred.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.makeInvestment().buildTransaction({
            'from': account.address,
            'nonce': web3.eth.get_transaction_count(account.address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
            'value': web3.to_wei(1, 'ether')  # Update to your desired investment amount
        })
        signed_txn = web3.eth.account.sign_transaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setRedemptionEvent(_timestamp: int):
    """Set the redemption event timestamp.

    Requires the timestamp as a parameter.
    
    Args:
        _timestamp (int): The timestamp for the redemption event.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.setRedemptionEvent(_timestamp).buildTransaction({
            'chainId': 1,  # Update to your desired chain ID
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(web3.eth.defaultAccount),
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def redeemShares():
    """Redeem shares from the contract.

    This function cannot be called by just anyone; it typically requires 
    proper conditions defined in the contract.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.redeemShares().buildTransaction({
            'chainId': 1,  # Update to your desired chain ID
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(web3.eth.defaultAccount),
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def distributeDividends(amount: int):
    """Distribute dividends to shareholders.

    Requires the amount to be distributed as a parameter.
    
    Args:
        amount (int): The amount of dividends to distribute.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.distributeDividends(amount).buildTransaction({
            'chainId': 1,  # Update to your desired chain ID
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(web3.eth.defaultAccount),
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def grantBoardSeat():
    """Grant a board seat to the investor.

    This function is typically called by the contract owner.
    
    Returns:
        dict: Transaction hash if successful, error message if failed.
    """
    try:
        txn = contract.functions.grantBoardSeat().buildTransaction({
            'chainId': 1,  # Update to your desired chain ID
            'gas': 2000000,
            'gasPrice': web3.toWei('50', 'gwei'),
            'nonce': web3.eth.getTransactionCount(web3.eth.defaultAccount),
        })
        signed_txn = web3.eth.account.signTransaction(txn, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStatus():
    """Get the current status of the contract.

    A view function that does not alter the state of the contract.
    
    Returns:
        dict: Current status if successful, error message if failed.
    """
    try:
        status = contract.functions.getStatus().call()
        return {"status": status}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def company():
    """Get the company address.

    A view function that returns the address of the company.
    
    Returns:
        dict: Company address if successful, error message if failed.
    """
    try:
        company_address = contract.functions.company().call()
        return {"company": company_address}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def investor():
    """Get the investor address.

    A view function that returns the address of the investor.
    
    Returns:
        dict: Investor address if successful, error message if failed.
    """
    try:
        investor_address = contract.functions.investor().call()
        return {"investor": investor_address}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def PURCHASE_PRICE_PER_SHARE():
    """Get the purchase price per share.

    A view function that returns the purchase price as a uint256.
    
    Returns:
        dict: Purchase price per share if successful, error message if failed.
    """
    try:
        price = contract.functions.PURCHASE_PRICE_PER_SHARE().call()
        return {"purchase_price_per_share": price}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def TOTAL_INVESTMENT_AMOUNT():
    """Get the total investment amount.

    A view function that retrieves the total amount invested in the contract.
    
    Returns:
        dict: Total investment amount if successful, error message if failed.
    """
    try:
        total_investment = contract.functions.TOTAL_INVESTMENT_AMOUNT().call()
        return {"total_investment_amount": total_investment}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def investmentTimestamp():
    """Get the timestamp of the investment.

    A view function that returns the timestamp of the latest investment.
    
    Returns:
        dict: Investment timestamp if successful, error message if failed.
    """
    try:
        timestamp = contract.functions.investmentTimestamp().call()
        return {"investment_timestamp": timestamp}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def redemptionEventTimestamp():
    """Get the redemption event timestamp.

    A view function that returns the timestamp of the redemption event.
    
    Returns:
        dict: Redemption event timestamp if successful, error message if failed.
    """
    try:
        timestamp = contract.functions.redemptionEventTimestamp().call()
        return {"redemption_event_timestamp": timestamp}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def sharesRedeemed():
    """Check if shares have been redeemed.

    A view function that returns a boolean indicating if shares have been redeemed.
    
    Returns:
        dict: True if shares have been redeemed, False otherwise, error message if failed.
    """
    try:
        redeemed = contract.functions.sharesRedeemed().call()
        return {"shares_redeemed": redeemed}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()