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
def areSharesRedeemed():
    """
    Check if shares are redeemed.
    No parameters required.
    Returns:
        {"result": bool}: Status of share redemption.
    """
    try:
        result = contract.functions.areSharesRedeemed().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestmentAmount():
    """
    Retrieve the total investment amount.
    No parameters required.
    Returns:
        {"result": uint256}: Total investment amount.
    """
    try:
        result = contract.functions.getInvestmentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePricePerShare():
    """
    Get the purchase price per share.
    No parameters required.
    Returns:
        {"result": uint256}: Purchase price per share.
    """
    try:
        result = contract.functions.getPurchasePricePerShare().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSharesQuantity():
    """
    Get the quantity of shares.
    No parameters required.
    Returns:
        {"result": uint256}: Quantity of shares.
    """
    try:
        result = contract.functions.getSharesQuantity().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makeInvestment():
    """
    Make an investment in the smart contract.
    No parameters required.
    Returns:
        {"tx_hash": hash}: Transaction hash of the investment.
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
    Redeem shares from the smart contract.
    No parameters required.
    Returns:
        {"tx_hash": hash}: Transaction hash of the shares redemption.
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

if __name__ == "__main__":
    mcp.run()