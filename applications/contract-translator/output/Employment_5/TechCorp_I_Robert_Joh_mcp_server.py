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
def terminateEmployment(reason: str):
    """
    Terminate employment with a specified reason.
    
    :param reason: The reason for termination.
    :return: Transaction hash of the termination.
    """
    try:
        txn = contract.functions.terminateEmployment(reason).buildTransaction({
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
def getFinancialTerms():
    """
    Get the financial terms of the employment contract.
    
    :return: A tuple containing salary, performance bonus, and stock options.
    """
    try:
        result = contract.functions.getFinancialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployeeObligations():
    """
    Get the obligations of the employee.
    
    :return: A list of employee obligations.
    """
    try:
        result = contract.functions.getEmployeeObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEmployerObligations():
    """
    Get the obligations of the employer.
    
    :return: A list of employer obligations.
    """
    try:
        result = contract.functions.getEmployerObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getSpecialTerms():
    """
    Get any special terms regarding the employment contract.
    
    :return: A list of special terms.
    """
    try:
        result = contract.functions.getSpecialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getTerminationConditions():
    """
    Get the conditions for termination of employment.
    
    :return: A list of termination conditions.
    """
    try:
        result = contract.functions.getTerminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def currentStatus():
    """
    Get the current status of the employment agreement.
    
    :return: The current status as an integer.
    """
    try:
        result = contract.functions.currentStatus().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employer():
    """
    Get the employer's address.
    
    :return: The employer's address.
    """
    try:
        result = contract.functions.employer().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employee():
    """
    Get the employee's address.
    
    :return: The employee's address.
    """
    try:
        result = contract.functions.employee().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def salary():
    """
    Get the employee's salary.
    
    :return: The salary as a uint256.
    """
    try:
        result = contract.functions.salary().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def performanceBonus():
    """
    Get the performance bonus for the employee.
    
    :return: The performance bonus as a uint256.
    """
    try:
        result = contract.functions.performanceBonus().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def stockOptions():
    """
    Get the stock options available to the employee.
    
    :return: The stock options as a uint256.
    """
    try:
        result = contract.functions.stockOptions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def commencementDate():
    """
    Get the commencement date of the employment.
    
    :return: The commencement date as a uint256.
    """
    try:
        result = contract.functions.commencementDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def endDate():
    """
    Get the end date of the employment.
    
    :return: The end date as a uint256.
    """
    try:
        result = contract.functions.endDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def status():
    """
    Get the status of the employment agreement.
    
    :return: The status as an integer.
    """
    try:
        result = contract.functions.status().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employeeObligations():
    """
    Get a list of obligations the employee must fulfill.
    
    :return: A list of employee obligations.
    """
    try:
        result = contract.functions.employeeObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def employerObligations():
    """
    Get a list of obligations the employer must fulfill.
    
    :return: A list of employer obligations.
    """
    try:
        result = contract.functions.employerObligations().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def specialTerms():
    """
    Get special terms regarding the employment contract.
    
    :return: A list of special terms.
    """
    try:
        result = contract.functions.specialTerms().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def terminationConditions():
    """
    Get conditions that dictate termination of employment.
    
    :return: A list of termination conditions.
    """
    try:
        result = contract.functions.terminationConditions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()