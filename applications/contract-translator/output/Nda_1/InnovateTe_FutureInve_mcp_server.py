import os
from web3 import Web3
from fastmcp import MCP, tool
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CONTRACT_ADDRESS = os.getenv("CONTRACT_ADDRESS")

# Set up Web3
web3 = Web3(Web3.HTTPProvider(RPC_URL))
assert web3.isConnected(), "Failed to connect to Web3 provider"

# Read ABI from file (assuming `abi.json` is the ABI file)
with open("abi.json", "r") as abi_file:
    contract_abi = abi_file.read()

# Initialize contract instance
contract = web3.eth.contract(address=Web3.to_checksum_address(CONTRACT_ADDRESS), abi=contract_abi)

# Initialize MCP server
mcp = MCP()

@tool()
def addObligation(description: str, penaltyForBreach: str):
    """
    Add an obligation to the NDA.

    Who can call it: landlord/tenant
    What it does: Adds an obligation to the NDA contract.
    
    Parameters:
        - description (str): Description of the obligation.
        - penaltyForBreach (str): Penalty for breaching this obligation.
        
    Returns:
        - dict: {"tx_hash": tx_hash} on success, or {"error": str(e)} on failure.
    """
    try:
        tx = contract.functions.addObligation(description, penaltyForBreach).buildTransaction({
            'from': web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
            'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def fulfillObligation(obligationIndex: int):
    """
    Fulfill an obligation in the NDA.

    Who can call it: landlord/tenant
    What it does: Marks an obligation as fulfilled.
    
    Parameters:
        - obligationIndex (int): Index of the obligation to fulfill.
        
    Returns:
        - dict: {"tx_hash": tx_hash} on success, or {"error": str(e)} on failure.
    """
    try:
        tx = contract.functions.fulfillObligation(obligationIndex).buildTransaction({
            'from': web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
            'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def getObligations():
    """
    Retrieve a list of all obligations from the NDA.

    Who can call it: anyone
    What it does: Fetches all obligations and their statuses.
    
    Returns:
        - list: A list of obligations, or {"error": str(e)} on failure.
    """
    try:
        obligations = contract.functions.getObligations().call()
        return obligations
    except Exception as e:
        return {"error": str(e)}

@tool()
def executeNDA():
    """
    Execute the NDA agreement.

    Who can call it: landlord/tenant
    What it does: Executes the NDA contract.
    
    Returns:
        - dict: {"tx_hash": tx_hash} on success, or {"error": str(e)} on failure.
    """
    try:
        tx = contract.functions.executeNDA().buildTransaction({
            'from': web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address,
            'nonce': web3.eth.getTransactionCount(web3.eth.account.privateKeyToAccount(PRIVATE_KEY).address),
            'gas': 2000000,
            'gasPrice': web3.toWei('20', 'gwei')
        })
        signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
        return {"tx_hash": tx_hash.hex()}
    except Exception as e:
        return {"error": str(e)}

@tool()
def getSpecialTerms():
    """
    Get special terms associated with the NDA.

    Who can call it: anyone
    What it does: Returns a list of special terms defined in the NDA.
    
    Returns:
        - list: List of special terms, or {"error": str(e)} on failure.
    """
    try:
        special_terms = contract.functions.getSpecialTerms().call()
        return special_terms
    except Exception as e:
        return {"error": str(e)}

@tool()
def owner():
    """
    Get the owner of the NDA contract.

    Who can call it: anyone
    What it does: Returns the owner address of the NDA.
    
    Returns:
        - str: Owner address, or {"error": str(e)} on failure.
    """
    try:
        owner_address = contract.functions.owner().call()
        return owner_address
    except Exception as e:
        return {"error": str(e)}

@tool()
def disclosingParty():
    """
    Get the details of the disclosing party.

    Who can call it: anyone
    What it does: Fetches information about the disclosing party.
    
    Returns:
        - dict: Disclosing party details, or {"error": str(e)} on failure.
    """
    try:
        party_info = contract.functions.disclosingParty().call()
        return party_info
    except Exception as e:
        return {"error": str(e)}

@tool()
def receivingParty():
    """
    Get the details of the receiving party.

    Who can call it: anyone
    What it does: Fetches information about the receiving party.
    
    Returns:
        - dict: Receiving party details, or {"error": str(e)} on failure.
    """
    try:
        party_info = contract.functions.receivingParty().call()
        return party_info
    except Exception as e:
        return {"error": str(e)}

@tool()
def startDate():
    """
    Get the start date of the NDA.

    Who can call it: anyone
    What it does: Fetches the start date of the NDA contract.
    
    Returns:
        - uint256: Start date as a timestamp, or {"error": str(e)} on failure.
    """
    try:
        start_date = contract.functions.startDate().call()
        return start_date
    except Exception as e:
        return {"error": str(e)}

@tool()
def confidentialityEnd():
    """
    Get the expiration date of the confidentiality.

    Who can call it: anyone
    What it does: Fetches the end date for confidentiality.
    
    Returns:
        - uint256: End date as a timestamp, or {"error": str(e)} on failure.
    """
    try:
        end_date = contract.functions.confidentialityEnd().call()
        return end_date
    except Exception as e:
        return {"error": str(e)}

@tool()
def obligations():
    """
    Get the list of obligations associated with the NDA.

    Who can call it: anyone
    What it does: Retrieves a list of obligations in the NDA contract.
    
    Returns:
        - list: List of obligations, or {"error": str(e)} on failure.
    """
    try:
        obligations_list = contract.functions.obligations().call()
        return obligations_list
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print("Starting MCP server for NDA Smart Contract...")
    mcp.run(transport="stdio")