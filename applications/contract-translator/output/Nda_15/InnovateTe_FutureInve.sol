// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    // State variables
    address public disclosingParty;
    address public receivingParty;
    uint public startDate;
    uint public endDate;
    string public obligationsDescription;
    string public disclosureExceptions;
    bool public hasFinancialTerms;

    event ObligationsFulfilled(string description);
    
    constructor() {
        // Assigning parties' addresses (address(0) in case of missing party)
        disclosingParty = address(0); 
        receivingParty = address(0);
        
        // Assigning default dates (0 for missing)
        startDate = 0;
        endDate = 0;
        
        // Setting default obligations and conditions descriptions
        obligationsDescription = "";
        disclosureExceptions = "";
        
        // Financial terms default status (false if missing)
        hasFinancialTerms = false;
    }

    // Getter functions
    function getDisclosingParty() external view returns (address) {
        return disclosingParty; // returns address, default is address(0)
    }

    function getReceivingParty() external view returns (address) {
        return receivingParty; // returns address, default is address(0)
    }

    function getStartDate() external view returns (uint) {
        return startDate; // returns uint, default is 0
    }

    function getEndDate() external view returns (uint) {
        return endDate; // returns uint, default is 0
    }
    
    function getObligationsDescription() external view returns (string memory) {
        return obligationsDescription; // returns string, default is ""
    }
    
    function getDisclosureExceptions() external view returns (string memory) {
        return disclosureExceptions; // returns string, default is ""
    }

    function hasFinancialTermsStatus() external view returns (bool) {
        return hasFinancialTerms; // returns bool, default is false
    }

    // Function to set parties
    function setParties(address _disclosingParty, address _receivingParty) external {
        if (_disclosingParty != address(0)) {
            disclosingParty = _disclosingParty;
        }
        if (_receivingParty != address(0)) {
            receivingParty = _receivingParty;
        }
    }

    // Function to set dates
    function setDates(uint _startDate, uint _endDate) external {
        if (_startDate > 0) {
            startDate = _startDate;
        }
        if (_endDate > 0) {
            endDate = _endDate;
        }
    }

    // Function to set obligations and conditions
    function setObligations(string memory _obligationsDescription, string memory _disclosureExceptions) external {
        if (bytes(_obligationsDescription).length > 0) {
            obligationsDescription = _obligationsDescription;
        }
        if (bytes(_disclosureExceptions).length > 0) {
            disclosureExceptions = _disclosureExceptions;
        }
    }

    // Function to set financial terms status
    function setFinancialTermsStatus(bool _hasFinancialTerms) external {
        hasFinancialTerms = _hasFinancialTerms;
    }

    // Function to fulfill obligations
    function fulfillObligations() external {
        // Perform checks or logic as required, for example, ensuring parties are set
        if (disclosingParty != address(0) && receivingParty != address(0)) {
            emit ObligationsFulfilled(obligationsDescription);
        }
    }

    // Function to handle termination conditions (example)
    function terminateAgreement() external {
        // Logic for termination can be implemented here
    }
}