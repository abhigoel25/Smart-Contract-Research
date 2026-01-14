// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvestmentAgreement {

    // State Variables
    struct Party {
        string name;
        address partyAddress;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate; // Using timestamp for date storage
    }

    struct Obligation {
        string party;
        string description;
        uint256 deadline; // Using timestamp for date storage
        string penaltyForBreach;
    }

    // Parties
    Party[2] private parties;
    
    // Financial Terms
    FinancialTerm[2] private financialTerms;
    
    // Obligations
    Obligation[] private obligations;

    // Events
    event AgreementCreated();
    event ObligationFulfilled(string party, string description);
    
    constructor() {
        // Initialize parties with defaults
        parties[0] = Party("BlockChain Innovations Inc.", address(0), "company");
        parties[1] = Party("Venture Capital Fund VII, LP", address(0), "company");
        
        // Initialize financial terms
        financialTerms[0] = FinancialTerm(10000000 ether, "USD", "purchase price", "one-time", 0); // Using ether for proper representation
        financialTerms[1] = FinancialTerm(8 ether, "USD", "purchase price per share", "", 0);
        
        // Initialize obligations
        obligations.push(Obligation("BlockChain Innovations Inc.", "must redeem shares if no qualified IPO by January 1, 2030", 1893561600, "redemption price includes accrued but unpaid dividends")); // Deadline: 2030-01-01
        obligations.push(Obligation("Venture Capital Fund VII, LP", "participate in the company sale if approved by majority holders", 0, ""));
        
        emit AgreementCreated();
    }
    
    // Getters for parties
    function getParty(uint8 index) public view returns (string memory, address, string memory) {
        if (index >= parties.length) {
            return ("", address(0), ""); // Return defaults for out-of-bounds index
        }
        return (parties[index].name, parties[index].partyAddress, parties[index].entityType);
    }

    // Getters for financial terms
    function getFinancialTerm(uint8 index) public view returns (uint256, string memory, string memory, string memory, uint256) {
        if (index >= financialTerms.length) {
            return (0, "", "", "", 0); // Return defaults for out-of-bounds index
        }
        return (financialTerms[index].amount, financialTerms[index].currency, financialTerms[index].purpose, financialTerms[index].frequency, financialTerms[index].dueDate);
    }

    // Getters for obligations
    function getObligation(uint8 index) public view returns (string memory, string memory, uint256, string memory) {
        if (index >= obligations.length) {
            return ("", "", 0, ""); // Return defaults for out-of-bounds index
        }
        return (obligations[index].party, obligations[index].description, obligations[index].deadline, obligations[index].penaltyForBreach);
    }

    // Action function to fulfill obligations
    function fulfillObligation(uint8 index) public {
        if (index >= obligations.length) return; // Return safely if index is out of bounds
        // Emit an event for fulfillment
        emit ObligationFulfilled(obligations[index].party, obligations[index].description);
        // Logic for fulfilling obligations could go here, if conditions allow
    }
    
    // Additional utility functions can be added as needed
}