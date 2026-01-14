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
    Allows the investor to make an investment.
    
    Returns:
        dict: Transaction hash of the investment transaction.
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
def redeemShares():
    """
    Allows the company to redeem shares.
    
    Returns:
        dict: Transaction hash of the redeem shares transaction.
    """
    try:
        txn = contract.functions.redeemShares().buildTransaction({
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
def getTotalInvestment():
    """
    Returns the total investment made by the investor.
    
    Returns:
        dict: Total investment as a uint256 value.
    """
    try:
        result = contract.functions.getTotalInvestment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSharePrice():
    """
    Returns the current share price.
    
    Returns:
        dict: Current share price as a uint256 value.
    """
    try:
        result = contract.functions.getSharePrice().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def company():
    """
    Returns the address of the company.
    
    Returns:
        dict: Company address as an Ethereum address.
    """
    try:
        result = contract.functions.company().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def investor():
    """
    Returns the address of the investor.
    
    Returns:
        dict: Investor address as an Ethereum address.
    """
    try:
        result = contract.functions.investor().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def totalInvestment():
    """
    Returns the total investment amount.
    
    Returns:
        dict: Total investment amount as a uint256 value.
    """
    try:
        result = contract.functions.totalInvestment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def sharePrice():
    """
    Returns the share price.
    
    Returns:
        dict: Share price as a uint256 value.
    """
    try:
        result = contract.functions.sharePrice().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def obligationsMet(addr):
    """
    Checks if obligations are met for a given address.
    
    Parameters:
        addr (address): The Ethereum address to check obligations against.
        
    Returns:
        dict: True if obligations are met, False otherwise.
    """
    try:
        result = contract.functions.obligationsMet(Web3.to_checksum_address(addr)).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()