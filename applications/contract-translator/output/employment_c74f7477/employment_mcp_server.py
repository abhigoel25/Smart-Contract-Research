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
abi_path = Path(__file__).parent / 'TechCorp_I_Robert_Joh.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("TechCorp_I_Robert_Joh")

@mcp.tool()
def getEmployer():
    """Retrieves the employer's address.
    
    Returns:
        dict: {'result': address} - The employer's address.
    """
    try:
        result = contract.functions.getEmployer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployee():
    """Retrieves the employee's address.
    
    Returns:
        dict: {'result': address} - The employee's address.
    """
    try:
        result = contract.functions.getEmployee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSalary():
    """Retrieves the salary amount.
    
    Returns:
        dict: {'result': amount} - The salary amount in wei.
    """
    try:
        result = contract.functions.getSalary().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getPerformanceBonus():
    """Retrieves the performance bonus amount.
    
    Returns:
        dict: {'result': amount} - The performance bonus amount in wei.
    """
    try:
        result = contract.functions.getPerformanceBonus().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStockOptions():
    """Retrieves the available stock options.
    
    Returns:
        dict: {'result': amount} - The number of stock options available.
    """
    try:
        result = contract.functions.getStockOptions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployerObligation(index):
    """Retrieves the employer's obligation at a specific index.
    
    Parameters:
        index (uint256): The index of the obligation.
        
    Returns:
        dict: {'result': obligation} - The employer's obligation as a string.
    """
    try:
        result = contract.functions.getEmployerObligation(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployeeObligation(index):
    """Retrieves the employee's obligation at a specific index.
    
    Parameters:
        index (uint256): The index of the obligation.
        
    Returns:
        dict: {'result': obligation} - The employee's obligation as a string.
    """
    try:
        result = contract.functions.getEmployeeObligation(index).call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()