// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got ';'
  --> <stdin>:47:38:
   |
47 |             partyAddress: address(0),; // Placeholder for address
   |                                      ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {

    struct Party {
        string name;
        string role;
        address partyAddress; // Address stored, defaults to address(0) if missing
        string email; // Optional field, defaults to empty string
        string entityType; // Optional field, defaults to empty string
    }

    struct Date {
        string dateType; // e.g. "start", "end"
        string value; // Human-readable date
        uint dayOfMonth; // day of the month, defaults to 0 if missing
    }

    struct Obligation {
        string party; // Name of the party responsible for the obligation
        string description; // Description of the obligation
        string deadline; // Optional field, defaults to empty string
        string penaltyForBreach; // Description of penalty
    }

    struct Condition {
        string exceptions; // Optional field, defaults to empty string
    }

    Party public disclosingParty;
    Party public receivingParty;

    Date public startDate;
    Date public endDate;

    Obligation public obligation; // Assuming a single obligation for simplicity
    Condition public conditions; // Handles all conditions in a single struct

    // Optional fields will have sensible defaults
    event NDACreated();

    constructor() {
        disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            role: "Disclosing Party",
            partyAddress: address(0),; // Placeholder for address
            email: "",; // Default to empty string
        });

        receivingParty = Party({
            name: "FutureInvest Capital Partners",
            role: "Receiving Party",
            partyAddress: address(0),; // Placeholder for address
            email: "",; // Default to empty string
        });

        // Dates with sensible defaults
        startDate = Date({
            value: "January 8, 2025",
        });

        endDate = Date({
            value: "January 8, 2028",
        });

        obligation = Obligation({
            party: "Receiving Party",
            description: "Maintain strict confidentiality, protect information with reasonable security measures, limit disclosure to employees/contractors with need-to-know on confidential basis, use information only for stated evaluation purposes, not reverse-engineer or attempt to derive underlying principles",
            deadline: "",; // Default to empty string
            penaltyForBreach: "Breach causes irreparable harm for which monetary damages are inadequate"
        });

        conditions = Condition({
            exceptions: "Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party when legally permitted."
        });

        emit NDACreated();
    }

    // Getters for parties
    function getDisclosingParty() public view returns (string memory, string memory, address, string memory, string memory) {
        return (disclosingParty.name,
            disclosingParty.entityType);
    }

    function getReceivingParty() public view returns (string memory, string memory, address, string memory, string memory) {
        return (receivingParty.name,
            receivingParty.entityType);
    }

    // Getters for dates
    function getStartDate() public view returns (string memory, uint) {
        return (startDate.value, startDate.dayOfMonth);