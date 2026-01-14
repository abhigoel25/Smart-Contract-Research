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
    """
    Retrieve the company information.

    Returns:
        dict: Contains the company name, address, and other details.
    """
    try:
        result = contract.functions.getCompany().call()
        return {"company_name": result[0], "company_address": result[1], "other_details": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestor():
    """
    Retrieve the investor information.

    Returns:
        dict: Contains the investor name, address, and other details.
    """
    try:
        result = contract.functions.getInvestor().call()
        return {"investor_name": result[0], "investor_address": result[1], "other_details": result[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePrice():
    """
    Retrieve the purchase price of the investment.

    Returns:
        dict: Contains the purchase price and associated details.
    """
    try:
        result = contract.functions.getPurchasePrice().call()
        return {"purchase_price": result[0], "other_details": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTotalInvestment():
    """
    Retrieve the total investment amount.

    Returns:
        dict: Contains the total investment and associated details.
    """
    try:
        result = contract.functions.getTotalInvestment().call()
        return {"total_investment": result[0], "other_details": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """
    Retrieve the start date of the investment.

    Returns:
        dict: Contains the start date and associated timestamp.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"start_date": result[0], "timestamp": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionTriggerDate():
    """
    Retrieve the redemption trigger date of the investment.

    Returns:
        dict: Contains the redemption trigger date and associated timestamp.
    """
    try:
        result = contract.functions.getRedemptionTriggerDate().call()
        return {"redemption_trigger_date": result[0], "timestamp": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillCompanyObligation(obligationDescription: str):
    """
    Fulfill a company obligation by providing a description.

    Args:
        obligationDescription (str): Description of the obligation to fulfill.

    Returns:
        dict: Transaction hash of the operation.
    """
    try:
        txn = contract.functions.fulfillCompanyObligation(obligationDescription).buildTransaction({
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
def getSpecialTerms():
    """
    Retrieve the special terms of the investment.

    Returns:
        dict: Contains an array of special terms.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"special_terms": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getConditions():
    """
    Retrieve the conditions of the investment.

    Returns:
        dict: Contains the primary and secondary conditions.
    """
    try:
        result = contract.functions.getConditions().call()
        return {"primary_condition": result[0], "secondary_condition": result[1]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """
    Retrieve the termination conditions of the investment.

    Returns:
        dict: Contains an array of termination conditions.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"termination_conditions": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()