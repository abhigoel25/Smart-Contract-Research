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
def fulfillObligations():
    """Fulfills obligations of the NDA contract.
    
    This function can be called by any party to fulfill their obligations.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.fulfillObligations().buildTransaction({
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
def getDisclosingParty():
    """Returns the address of the disclosing party.
    
    This function can be called by anyone to view the disclosing party's address.
    Returns the disclosing party's address.
    """
    try:
        result = contract.functions.getDisclosingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getEndDate():
    """Returns the end date of the NDA contract.
    
    This function can be called by anyone to view the end date.
    Returns the end date as a timestamp.
    """
    try:
        result = contract.functions.getEndDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getObligationsDescription():
    """Returns the obligations description of the NDA.
    
    This function can be called by anyone to view the obligations description.
    Returns the obligations description as a string.
    """
    try:
        result = contract.functions.getObligationsDescription().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getReceivingParty():
    """Returns the address of the receiving party.
    
    This function can be called by anyone to view the receiving party's address.
    Returns the receiving party's address.
    """
    try:
        result = contract.functions.getReceivingParty().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getStartDate():
    """Returns the start date of the NDA contract.
    
    This function can be called by anyone to view the start date.
    Returns the start date as a timestamp.
    """
    try:
        result = contract.functions.getStartDate().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def getDisclosureExceptions():
    """Returns the disclosure exceptions of the NDA.
    
    This function can be called by anyone to view the disclosure exceptions.
    Returns the disclosure exceptions as a string.
    """
    try:
        result = contract.functions.getDisclosureExceptions().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def hasFinancialTermsStatus():
    """Returns whether the NDA has financial terms status.
    
    This function can be called by anyone to view the financial terms status.
    Returns true if financial terms exist, false otherwise.
    """
    try:
        result = contract.functions.hasFinancialTermsStatus().call()
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

@mcp.tool()
def setParties(_disclosingParty: str, _receivingParty: str):
    """Sets the disclosing and receiving parties of the NDA.
    
    This function can only be called by authorized parties.
    Parameters:
        _disclosingParty: Address of the disclosing party.
        _receivingParty: Address of the receiving party.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.setParties(Web3.to_checksum_address(_disclosingParty), Web3.to_checksum_address(_receivingParty)).buildTransaction({
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
def setDates(_startDate: int, _endDate: int):
    """Sets the start and end dates of the NDA.
    
    This function can only be called by authorized parties.
    Parameters:
        _startDate: Timestamp for the start date.
        _endDate: Timestamp for the end date.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.setDates(_startDate, _endDate).buildTransaction({
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
def setObligations(_obligationsDescription: str, _disclosureExceptions: str):
    """Sets the obligations description and disclosure exceptions of the NDA.
    
    This function can only be called by authorized parties.
    Parameters:
        _obligationsDescription: Obligations description as a string.
        _disclosureExceptions: Disclosure exceptions as a string.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.setObligations(_obligationsDescription, _disclosureExceptions).buildTransaction({
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
def setFinancialTermsStatus(_hasFinancialTerms: bool):
    """Sets the financial terms status of the NDA.
    
    This function can only be called by authorized parties.
    Parameters:
        _hasFinancialTerms: Boolean indicating the status of financial terms.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.setFinancialTermsStatus(_hasFinancialTerms).buildTransaction({
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
def terminateAgreement():
    """Terminates the NDA agreement.
    
    This function can only be called by authorized parties.
    Returns the transaction hash of the transaction.
    """
    try:
        txn = contract.functions.terminateAgreement().buildTransaction({
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

if __name__ == "__main__":
    mcp.run()