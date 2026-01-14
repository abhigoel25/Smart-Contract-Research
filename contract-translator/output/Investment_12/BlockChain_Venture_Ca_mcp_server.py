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
    """Retrieve the company's details.

    Returns:
        dict: Contains company name, additional info, address, and description.
    """
    try:
        result = contract.functions.getCompany().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestor():
    """Retrieve the investor's details.

    Returns:
        dict: Contains investor name, additional info, address, and description.
    """
    try:
        result = contract.functions.getInvestor().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTotalInvestment():
    """Retrieve the total investment details.

    Returns:
        dict: Contains total investment amount and related information.
    """
    try:
        result = contract.functions.getTotalInvestment().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePrice():
    """Retrieve the current purchase price details.

    Returns:
        dict: Contains purchase price and related information.
    """
    try:
        result = contract.functions.getPurchasePrice().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Retrieve the start date details.

    Returns:
        dict: Contains start date and related information.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionTriggerDate():
    """Retrieve the redemption trigger date details.

    Returns:
        dict: Contains redemption trigger date and related information.
    """
    try:
        result = contract.functions.getRedemptionTriggerDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSeriesAStock():
    """Retrieve Series A stock details.

    Returns:
        dict: Contains Series A stock information.
    """
    try:
        result = contract.functions.getSeriesAStock().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionObligation():
    """Retrieve redemption obligation details.

    Returns:
        dict: Contains redemption obligation information.
    """
    try:
        result = contract.functions.getRedemptionObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def triggerInvestment():
    """Trigger an investment process.

    Returns:
        dict: Contains transaction hash of the investment trigger.
    """
    try:
        txn = contract.functions.triggerInvestment().buildTransaction({
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
    """Redeem shares in the investment.

    Returns:
        dict: Contains transaction hash of the shares redemption.
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
def parseDate(dateValue: str):
    """Parse a date string into a timestamp.

    Args:
        dateValue (str): The date string to parse.

    Returns:
        dict: Contains the parsed timestamp.
    """
    try:
        result = contract.functions.parseDate(dateValue).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()