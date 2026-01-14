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
    """Retrieve the employer's address.

    Returns:
        dict: Contains the employer's address.
    """
    try:
        result = contract.functions.getEmployer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployee():
    """Retrieve the employee's address.

    Returns:
        dict: Contains the employee's address.
    """
    try:
        result = contract.functions.getEmployee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSalaryAmount():
    """Retrieve the salary amount.

    Returns:
        dict: Contains the salary amount.
    """
    try:
        result = contract.functions.getSalaryAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getMonthlyPaymentAmount():
    """Retrieve the monthly payment amount.

    Returns:
        dict: Contains the monthly payment amount.
    """
    try:
        result = contract.functions.getMonthlyPaymentAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getBonusAmount():
    """Retrieve the bonus amount.

    Returns:
        dict: Contains the bonus amount.
    """
    try:
        result = contract.functions.getBonusAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStockOptionsAmount():
    """Retrieve the stock options amount.

    Returns:
        dict: Contains the stock options amount.
    """
    try:
        result = contract.functions.getStockOptionsAmount().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployeeObligation():
    """Retrieve the employee's obligations description.

    Returns:
        dict: Contains the employee obligation description.
    """
    try:
        result = contract.functions.getEmployeeObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployerObligation():
    """Retrieve the employer's obligations description.

    Returns:
        dict: Contains the employer obligation description.
    """
    try:
        result = contract.functions.getEmployerObligation().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()