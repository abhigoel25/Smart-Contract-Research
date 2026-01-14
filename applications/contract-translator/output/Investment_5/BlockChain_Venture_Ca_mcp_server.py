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
def makeInvestment():
    """
    Makes an investment in the contract.
    
    This function can be called by the investor to make an investment.
    
    Returns:
        dict: A dictionary with the transaction hash.
    """
    try:
        txn = contract.functions.makeInvestment().buildTransaction({
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
def redeemShares(quantity: int):
    """
    Redeems shares held by the investor.
    
    Parameters:
        quantity (int): The number of shares to redeem.
    
    Returns:
        dict: A dictionary with the transaction hash.
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
def getCompany():
    """
    Gets the address of the company.
    
    Returns:
        dict: A dictionary with the company address.
    """
    try:
        result = contract.functions.getCompany().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestor():
    """
    Gets the address of the investor.
    
    Returns:
        dict: A dictionary with the investor address.
    """
    try:
        result = contract.functions.getInvestor().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestmentAmount():
    """
    Gets the total investment amount made.
    
    Returns:
        dict: A dictionary with the investment amount.
    """
    try:
        result = contract.functions.getInvestmentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePricePerShare():
    """
    Gets the purchase price per share.
    
    Returns:
        dict: A dictionary with the purchase price per share.
    """
    try:
        result = contract.functions.getPurchasePricePerShare().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSharesQuantity():
    """
    Gets the number of shares currently held.
    
    Returns:
        dict: A dictionary with the shares quantity.
    """
    try:
        result = contract.functions.getSharesQuantity().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def isSharesRedeemed():
    """
    Checks if shares have been redeemed.
    
    Returns:
        dict: A dictionary indicating whether shares are redeemed.
    """
    try:
        result = contract.functions.isSharesRedeemed().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()