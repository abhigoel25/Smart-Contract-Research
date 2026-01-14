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
def getCompanyAddress():
    """Get the company address.
    
    Returns:
        dict: The company address.
    """
    try:
        result = contract.functions.getCompanyAddress().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestorAddress():
    """Get the investor address.
    
    Returns:
        dict: The investor address.
    """
    try:
        result = contract.functions.getInvestorAddress().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestmentAmount():
    """Get the amount of investment.
    
    Returns:
        dict: The amount of investment.
    """
    try:
        result = contract.functions.getInvestmentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPurchasePricePerShare():
    """Get the purchase price per share.
    
    Returns:
        dict: The purchase price per share.
    """
    try:
        result = contract.functions.getPurchasePricePerShare().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Get the start date of the investment.
    
    Returns:
        dict: The start date.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getRedemptionTriggerDate():
    """Get the redemption trigger date.
    
    Returns:
        dict: The redemption trigger date.
    """
    try:
        result = contract.functions.getRedemptionTriggerDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getCompanyObligation():
    """Get the company's obligation.
    
    Returns:
        dict: The company's obligation.
    """
    try:
        result = contract.functions.getCompanyObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getInvestorObligation():
    """Get the investor's obligation.
    
    Returns:
        dict: The investor's obligation.
    """
    try:
        result = contract.functions.getInvestorObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def makeInvestment(amount: int):
    """Make an investment.
    
    Args:
        amount (int): The investment amount in wei.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.makeInvestment(amount).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillCompanyObligation():
    """Fulfill the company's obligation.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.fulfillCompanyObligation().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def fulfillInvestorObligation():
    """Fulfill the investor's obligation.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.fulfillInvestorObligation().buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setAddresses(companyAddress: str, investorAddress: str):
    """Set the company and investor addresses.
    
    Args:
        companyAddress (str): The company address.
        investorAddress (str): The investor address.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.setAddresses(Web3.to_checksum_address(companyAddress), Web3.to_checksum_address(investorAddress)).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setFinancialTerms(investmentAmount: int, purchasePricePerShare: int):
    """Set the financial terms of the investment.
    
    Args:
        investmentAmount (int): The investment amount.
        purchasePricePerShare (int): The purchase price per share.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.setFinancialTerms(investmentAmount, purchasePricePerShare).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setDates(startDate: int, redemptionTriggerDate: int):
    """Set the start and redemption trigger dates.
    
    Args:
        startDate (int): The start date as a timestamp.
        redemptionTriggerDate (int): The redemption trigger date as a timestamp.
    
    Returns:
        dict: The transaction hash.
    """
    try:
        txn = contract.functions.setDates(startDate, redemptionTriggerDate).buildTransaction({
            'from': account_address,
            'nonce': web3.eth.get_transaction_count(account_address),
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
        tx_hash = web3.eth.send_transaction(txn)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()