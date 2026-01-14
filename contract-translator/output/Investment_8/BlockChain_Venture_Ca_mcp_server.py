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
    Make an investment in the contract.
    Can be called by any authorized user.
    Returns the transaction hash of the investment transaction.
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
    Redeem shares from the contract.
    Can be called by any authorized user.
    Returns the transaction hash of the shares redemption transaction.
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
def getInvestmentDetails():
    """
    Get the investment details from the contract.
    Can be called by anyone.
    Returns a tuple of (companyAddress, investorAddress, totalInvestment, purchasePricePerShare, totalShares, redemptionDeadline).
    """
    try:
        result = contract.functions.getInvestmentDetails().call()
        return {
            "companyAddress": result[0],
            "investorAddress": result[1],
            "totalInvestment": result[2],
            "purchasePricePerShare": result[3],
            "totalShares": result[4],
            "redemptionDeadline": result[5]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()