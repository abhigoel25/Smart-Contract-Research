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
abi_path = Path(__file__).parent / 'BlockChain_Venture_Ca.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def getCompany():
    """Retrieve company details.
    
    Returns:
        dict: Company details including name, type, address, description, and additional info.
    """
    try:
        result = contract.functions.getCompany().call()
        return {
            "name": result[0],
            "type": result[1],
            "address": result[2],
            "description": result[3],
            "additionalInfo": result[4],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestor():
    """Retrieve investor details.
    
    Returns:
        dict: Investor details including name, type, address, description, and additional info.
    """
    try:
        result = contract.functions.getInvestor().call()
        return {
            "name": result[0],
            "type": result[1],
            "address": result[2],
            "description": result[3],
            "additionalInfo": result[4],
        }
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestmentAmount():
    """Get the total investment amount.
    
    Returns:
        dict: Total investment amount as a uint256.
    """
    try:
        result = contract.functions.getInvestmentAmount().call()
        return {"investmentAmount": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePrice():
    """Get the purchase price.
    
    Returns:
        dict: Purchase price as a uint256.
    """
    try:
        result = contract.functions.getPurchasePrice().call()
        return {"purchasePrice": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Get the investment start date.
    
    Returns:
        dict: Start date as a string.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"startDate": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionTriggerDate():
    """Get the redemption trigger date.
    
    Returns:
        dict: Redemption trigger date as a string.
    """
    try:
        result = contract.functions.getRedemptionTriggerDate().call()
        return {"redemptionTriggerDate": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def invest():
    """Invest in the venture capital.
    
    Returns:
        dict: Transaction hash if successful.
    """
    try:
        txn = contract.functions.invest().buildTransaction({
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
def redeemShares(quantity):
    """Redeem a specific quantity of shares.
    
    Parameters:
        quantity (uint256): The number of shares to redeem.

    Returns:
        dict: Transaction hash if successful.
    """
    try:
        txn = contract.functions.redeemShares(quantity).buildTransaction({
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
def performObligation():
    """Perform contractual obligations.
    
    Returns:
        dict: Transaction hash if successful.
    """
    try:
        txn = contract.functions.performObligation().buildTransaction({
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
def addSpecialTerm(term):
    """Add a special term to the contract.
    
    Parameters:
        term (string): The special term to add.

    Returns:
        dict: Transaction hash if successful.
    """
    try:
        txn = contract.functions.addSpecialTerm(term).buildTransaction({
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

if __name__ == "__main__":
    mcp.run()