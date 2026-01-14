// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected ',' but got ';'
  --> <stdin>:60:35:
   |
60 |             return ("", address(0);
   |                                   ^
// This contract failed to compile after 3 fix attempts

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
        financialTerms[0] = FinancialTerm(10000000 ether, "USD", "purchase price", "one-time", 0); // Using ether for proper representation;
        financialTerms[1] = FinancialTerm(8 ether, "USD", "purchase price per share", "", 0);

        // Initialize obligations
        obligations.push(Obligation("BlockChain Innovations Inc.", "must redeem shares if no qualified IPO by January 1, 2030", 1893561600, "redemption price includes accrued but unpaid dividends")); // Deadline: 2030-01-01
        obligations.push(Obligation("Venture Capital Fund VII, LP", "participate in the company sale if approved by majority holders", 0, ""));

        emit AgreementCreated();
    }

    // Getters for parties
    function getParty(uint8 index) public view returns (string memory, address, string memory) {
        if (index >= parties.length) {
            return ("", address(0);