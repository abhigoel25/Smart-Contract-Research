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
abi_path = Path(__file__).parent / 'investment.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account_address = Web3.to_checksum_address(os.getenv('ACCOUNT_ADDRESS'))
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("BlockChain_Venture_Ca")

@mcp.tool()
def getAntiDilutionCondition():
    """ 
    Retrieves the anti-dilution condition of the investment.
    
    Returns:
        dict: A dictionary containing the anti-dilution condition.
    """
    try:
        result = contract.functions.getAntiDilutionCondition().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getCompanyAddress():
    """ 
    Retrieves the address of the company involved in the investment.
    
    Returns:
        dict: A dictionary containing the company address.
    """
    try:
        result = contract.functions.getCompanyAddress().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestorAddress():
    """ 
    Retrieves the address of the investor involved in the investment.
    
    Returns:
        dict: A dictionary containing the investor address.
    """
    try:
        result = contract.functions.getInvestorAddress().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligation():
    """ 
    Retrieves the obligations associated with the investment as a tuple.
    
    Returns:
        dict: A dictionary containing the obligation details.
    """
    try:
        result = contract.functions.getObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getProductDevelopmentAmount():
    """ 
    Retrieves the amount allocated for product development.
    
    Returns:
        dict: A dictionary containing the product development amount.
    """
    try:
        result = contract.functions.getProductDevelopmentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePricePerShare():
    """ 
    Retrieves the purchase price per share of the investment.
    
    Returns:
        dict: A dictionary containing the purchase price per share.
    """
    try:
        result = contract.functions.getPurchasePricePerShare().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionTriggerDate():
    """ 
    Retrieves the redemption trigger date.
    
    Returns:
        dict: A dictionary containing the redemption trigger date.
    """
    try:
        result = contract.functions.getRedemptionTriggerDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSalesAndMarketingAmount():
    """ 
    Retrieves the amount allocated for sales and marketing.
    
    Returns:
        dict: A dictionary containing the sales and marketing amount.
    """
    try:
        result = contract.functions.getSalesAndMarketingAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """ 
    Retrieves special terms associated with the investment.
    
    Returns:
        dict: A dictionary containing the special terms as a list.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """ 
    Retrieves the start date of the investment.
    
    Returns:
        dict: A dictionary containing the start date.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getWorkingCapitalReserveAmount():
    """ 
    Retrieves the amount allocated for working capital reserve.
    
    Returns:
        dict: A dictionary containing the working capital reserve amount.
    """
    try:
        result = contract.functions.getWorkingCapitalReserveAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def processInvestment(purpose, amount):
    """ 
    Processes an investment transaction.
    
    Args:
        purpose (str): The purpose of the investment.
        amount (int): The amount to invest.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.processInvestment(purpose, amount).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def redeemShares():
    """ 
    Redeems shares for the investor.
    
    Returns:
        dict: A dictionary containing the transaction hash.
    """
    try:
        txn = contract.functions.redeemShares().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()