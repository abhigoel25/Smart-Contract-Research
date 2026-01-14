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
abi_path = Path(__file__).parent / 'InnovateTe_FutureInve.abi.json'
with open(abi_path, 'r') as f:
    contract_abi = json.load(f)

RPC_URL = os.getenv('RPC_URL')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')
CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')

web3 = Web3(Web3.HTTPProvider(RPC_URL))
account = web3.eth.account.from_key(PRIVATE_KEY)
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

mcp = FastMCP("InnovateTe_FutureInve")

@mcp.tool()
def addObligation(description: str, penalty: str) -> dict:
    """Add an obligation to the NDA.
    
    Parameters:
        description (str): Description of the obligation.
        penalty (str): Penalty for breach of the obligation.
        
    Returns:
        dict: Transaction hash of the executed function or error message.
    """
    try:
        txn = contract.functions.addObligation(description, penalty).buildTransaction({
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
def finalizeAgreement() -> dict:
    """Finalize the NDA agreement between the parties.
    
    Returns:
        dict: Transaction hash of the executed function or error message.
    """
    try:
        txn = contract.functions.finalizeAgreement().buildTransaction({
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
def reportBreach(description: str) -> dict:
    """Report a breach of the NDA.
    
    Parameters:
        description (str): Description of the breach.
        
    Returns:
        dict: Transaction hash of the executed function or error message.
    """
    try:
        txn = contract.functions.reportBreach(description).buildTransaction({
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
def getObligations() -> dict:
    """Retrieve the obligations from the NDA.
    
    Returns:
        dict: List of obligations or error message.
    """
    try:
        obligations = contract.functions.getObligations().call()
        return {"obligations": obligations}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def disclosingParty() -> dict:
    """Retrieve the disclosing party information.
    
    Returns:
        dict: Name, role, and address of the disclosing party or error message.
    """
    try:
        party_info = contract.functions.disclosingParty().call()
        return {"name": party_info[0], "role": party_info[1], "addressLine": party_info[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def receivingParty() -> dict:
    """Retrieve the receiving party information.
    
    Returns:
        dict: Name, role, and address of the receiving party or error message.
    """
    try:
        party_info = contract.functions.receivingParty().call()
        return {"name": party_info[0], "role": party_info[1], "addressLine": party_info[2]}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def obligations() -> dict:
    """Retrieve all obligations in the NDA.
    
    Returns:
        dict: List of all obligations or error message.
    """
    try:
        obligations = contract.functions.obligations().call()
        return {"obligations": obligations}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def terms() -> dict:
    """Retrieve the terms of the NDA.
    
    Returns:
        dict: Special terms and termination conditions of the NDA or error message.
    """
    try:
        special_terms, termination_conditions = contract.functions.terms().call()
        return {"specialTerms": special_terms, "terminationConditions": termination_conditions}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def startDate() -> dict:
    """Retrieve the start date of the NDA.
    
    Returns:
        dict: Start date as a timestamp or error message.
    """
    try:
        start_date = contract.functions.startDate().call()
        return {"startDate": start_date}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def confidentialityPeriodEnd() -> dict:
    """Retrieve the end date of the confidentiality period.
    
    Returns:
        dict: End date as a timestamp or error message.
    """
    try:
        end_date = contract.functions.confidentialityPeriodEnd().call()
        return {"confidentialityPeriodEnd": end_date}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def isActive() -> dict:
    """Check if the NDA is currently active.
    
    Returns:
        dict: Boolean status of the NDA or error message.
    """
    try:
        active_status = contract.functions.isActive().call()
        return {"isActive": active_status}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    mcp.run()