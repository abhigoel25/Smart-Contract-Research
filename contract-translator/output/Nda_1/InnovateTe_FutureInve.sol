// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    // Party Struct
    struct Party {
        string name;
        string role;
        string addr;
    }

    // Obligation Struct
    struct Obligation {
        string description;
        string penaltyForBreach;
        bool isFulfilled;
    }

    // Events
    event ObligationAdded(string partyRole, string description);
    event ObligationFulfilled(string partyRole, string description);
    event NDAExecuted(string disclosingParty, string receivingParty, uint256 startDate, uint256 confidentialityEnd);

    address public owner;
    Party public disclosingParty;
    Party public receivingParty;
    uint256 public startDate;
    uint256 public confidentialityEnd;
    Obligation[] public obligations;

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the contract owner can perform this action.");
        _;
    }

    // Constructor
    constructor() {
        owner = msg.sender;
        disclosingParty = Party("InnovateTech Ventures, LLC", "Disclosing Party", "333 Startup Way, San Francisco, CA 94105");
        receivingParty = Party("FutureInvest Capital Partners", "Receiving Party", "777 Investment Drive, New York, NY 10005");
        startDate = 1704672000; // 2025-01-08 in timestamp
        confidentialityEnd = 1704672000 + 3 * 365 days; // 3 years from start date
    }

    // Add an obligation
    function addObligation(string memory _description, string memory _penaltyForBreach) public onlyOwner {
        obligations.push(Obligation({
            description: _description,
            penaltyForBreach: _penaltyForBreach,
            isFulfilled: false
        }));
        emit ObligationAdded(receivingParty.role, _description);
    }

    // Mark an obligation as fulfilled
    function fulfillObligation(uint256 obligationIndex) public {
        require(obligationIndex < obligations.length, "Invalid obligation index.");
        require(!obligations[obligationIndex].isFulfilled, "Obligation already fulfilled.");

        obligations[obligationIndex].isFulfilled = true;
        emit ObligationFulfilled(receivingParty.role, obligations[obligationIndex].description);
    }

    // Get current obligations
    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }

    // NDA Execution Log
    function executeNDA() public onlyOwner {
        emit NDAExecuted(disclosingParty.name, receivingParty.name, startDate, confidentialityEnd);
    }

    // Special terms and termination conditions can be added as public variables or functions if needed.
    
    // Example function to view the special terms
    function getSpecialTerms() public pure returns (string[] memory) {
        string[] memory terms = new string[](2);
        terms[0] = "Excludes public domain information, independently developed information, and information rightfully received from third parties.";
        terms[1] = "Receiving Party may disclose if required by law/court order after prior written notice to Disclosing Party.";
        return terms;
    }
}