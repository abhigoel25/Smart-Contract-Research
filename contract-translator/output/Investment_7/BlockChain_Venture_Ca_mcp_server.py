import os
import json
from pathlib import Path
from web3 import Web3
from dotenv import load_dotenv
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
    Initiates an investment in the contract.
    Can be called by an investor.

    Returns:
        dict: Transaction hash of the investment.
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
    Redeems shares in the contract.
    Can be called by the company.

    Returns:
        dict: Transaction hash of the share redemption.
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
def isSharesRedeemed():
    """
    Checks if shares have been redeemed.

    Returns:
        dict: True if shares are redeemed, otherwise False.
    """
    try:
        result = contract.functions.isSharesRedeemed().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestmentDetails():
    """
    Retrieves the investment details.

    Returns:
        dict: Investment amount and purchase price per share.
    """
    try:
        result = contract.functions.getInvestmentDetails().call()
        return {"investment_amount": result[0], "purchase_price": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def company():
    """
    Retrieves the company address.

    Returns:
        dict: Address of the company.
    """
    try:
        result = contract.functions.company().call()
        return {"company": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def investor():
    """
    Retrieves the investor address.

    Returns:
        dict: Address of the investor.
    """
    try:
        result = contract.functions.investor().call()
        return {"investor": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def investmentAmount():
    """
    Retrieves the investment amount.

    Returns:
        dict: Amount of investment.
    """
    try:
        result = contract.functions.investmentAmount().call()
        return {"investment_amount": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def purchasePricePerShare():
    """
    Retrieves the purchase price per share.

    Returns:
        dict: Purchase price per share.
    """
    try:
        result = contract.functions.purchasePricePerShare().call()
        return {"purchase_price": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def sharesRedeemed():
    """
    Checks if shares have been redeemed.

    Returns:
        dict: True if shares are redeemed, otherwise False.
    """
    try:
        result = contract.functions.sharesRedeemed().call()
        return {"shares_redeemed": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()