// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got 'address'
 --> <stdin>:9:16:
  |
9 |         string address;
  |                ^^^^^^^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    // State variables
    struct Party {
        string name;
        string role;
        string address;
        string email; // Optional
        string entityType;
    }

    struct Date {
        string dateType;
        string value;
        uint dayOfMonth;
    }

    struct Obligation {
        string party;
        string description;
        string deadline; // Optional
        string penaltyForBreach;
    }

    Party public disclosingParty;
    Party public receivingParty;

    Date public startDate;
    Date public endDate;

    Obligation public receivingPartyObligation;

    event AgreementExecuted();

    constructor() {
        // Initialize disclosing party
        disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            role: "Disclosing Party",
            address: "333 Startup Way, San Francisco, CA 94105",
        });

        // Initialize receiving party
        receivingParty = Party({
            name: "FutureInvest Capital Partners",
            role: "Receiving Party",
            address: "777 Investment Drive, New York, NY 10005",
        });

        // Initialize dates
        startDate = Date({
            value: "2025-01-08",
        });

        endDate = Date({
            value: "2028-01-08",
        });

        // Initialize obligation for receiving party
        receivingPartyObligation = Obligation({
            party: "Receiving Party",
            description: "Maintain strict confidentiality, protect information with reasonable security measures, limit disclosure to employees/contractors with need-to-know on confidential basis, use information only for stated evaluation purposes, not reverse-engineer or attempt to derive underlying principles.",
            penaltyForBreach: "Breach causes irreparable harm for which monetary damages are inadequate."
        });
    }

    // Getters for all parties
    function getDisclosingParty() public view returns (string memory name, string memory role, string memory addr, string memory email) {
        name = disclosingParty.name;
        role = disclosingParty.role;
        addr = disclosingParty.address;
        email = disclosingParty.email;
    }

    function getReceivingParty() public view returns (string memory name, string memory role, string memory addr, string memory email) {
        name = receivingParty.name;
        role = receivingParty.role;
        addr = receivingParty.address;
        email = receivingParty.email;
    }

    // Getters for dates
    function getStartDate() public view returns (string memory dateType, string memory value, uint dayOfMonth) {
        dateType = startDate.dateType;
        value = startDate.value;
        dayOfMonth = startDate.dayOfMonth;
    }

    function getEndDate() public view returns (string memory dateType, string memory value, uint dayOfMonth) {
        dateType = endDate.dateType;
        value = endDate.value;
        dayOfMonth = endDate.dayOfMonth;
    }

    // Action function for obligations
    function fulfillObligation() public {
        // Logic to fulfill the obligation
        // This could include conditions based on certain states, 
        // but we avoid reverting due to missing data
        if(keccak256(abi.encodePacked(receivingPartyObligation.description)) != keccak256(abi.encodePacked(""))) {
            emit AgreementExecuted();
        }
    }
}