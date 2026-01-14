// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected identifier but got 'address'
 --> <stdin>:8:16:
  |
8 |         string address; // Directly store address as string for simplicty
  |                ^^^^^^^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    struct Party {
        string name;
        string role;
        string address; // Directly store address as string for simplicty
        string email; // Optional
        string entityType;
    }

    struct Obligation {
        string party;
        string description;
        string deadline; // Optional
        string penaltyForBreach; // Optional
    }

    string public title;
    Party public disclosingParty;
    Party public receivingParty;
    uint public startDate; // Timestamp in seconds
    string[] public specialTerms;
    string public exceptionConditions;
    string[] public terminationConditions;
    Obligation[] public obligations;

    event ContractCreated(string title);
    event ObligationAdded(string description);

    constructor() {
        title = "MUTUAL NON-DISCLOSURE AGREEMENT";

        // Set parties with defaults
        disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            role: "Disclosing Party",
            address: "333 Startup Way, San Francisco, CA 94105",
            email: "",; // Optional
        });

        receivingParty = Party({
            name: "FutureInvest Capital Partners",
            role: "Receiving Party",
            address: "777 Investment Drive, New York, NY 10005",
            email: "",; // Optional
        });

        // Set the start date
        startDate = 1736572800; // Example timestamp for January 8, 2025;

        // Populate obligations
        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Maintain strict confidentiality and protect information with reasonable security measures.",
            deadline: "",; // Optional
            penaltyForBreach: "Irreparable harm for which monetary damages are inadequate."
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Limit disclosure to employees/contractors with need-to-know on a confidential basis.",
            deadline: "",; // Optional
            penaltyForBreach: ""; // Optional
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Use information only for stated evaluation purposes.",
            deadline: "",; // Optional
            penaltyForBreach: ""; // Optional
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Not reverse-engineer or attempt to derive underlying principles.",
            deadline: "",; // Optional
            penaltyForBreach: ""; // Optional
        }));

        // Populate special terms
        specialTerms.push("Confidentiality Period: 3 years from disclosure date.");
        specialTerms.push("Obligations survive termination of discussions.");
        specialTerms.push("Trade Secrets are protected for as long as they remain trade secrets under applicable law.");

        // Set exception conditions
        exceptionConditions = "Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party.";

        // Populate termination conditions
        terminationConditions.push("Discussions can be terminated at any time but obligations survive termination.");

        emit ContractCreated(title);
    }

    // VIEW FUNCTIONS
    function getDisclosingParty() public view returns (string memory, string memory, string memory, string memory, string memory) {
        return (disclosingParty.name, disclosingParty.role, disclosingParty.address, disclosingParty.email, disclosingParty.entityType);