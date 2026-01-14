// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNDA {
    enum Party { Disclosing, Receiving }

    struct Participant {
        string name;
        Party role;
        string addressLine;
    }

    struct Obligation {
        string description;
        string penaltyForBreach;
    }

    struct Terms {
        string[] specialTerms;
        string[] terminationConditions;
    }

    Participant public disclosingParty;
    Participant public receivingParty;
    Obligation[] public obligations;
    Terms public terms;
    
    uint256 public startDate;
    uint256 public confidentialityPeriodEnd;
    bool public isActive;

    event ObligationAdded(string description);
    event AgreementFinalized(string indexed disclosingParty, string indexed receivingParty);
    event BreachReported(string indexed partyBreach, string description);

    modifier onlyActive() {
        require(isActive, "Contract is not active.");
        _;
    }

    modifier onlyDisclosingParty() {
        require(
            msg.sender == address(this), // Placeholder for actual disclosing party address check
            "Only the Disclosing Party can call this function."
        );
        _;
    }

    modifier onlyReceivingParty() {
        require(
            msg.sender == address(this), // Placeholder for actual receiving party address check
            "Only the Receiving Party can call this function."
        );
        _;
    }

    constructor() {
        disclosingParty = Participant({
            name: "InnovateTech Ventures, LLC",
            role: Party.Disclosing,
            addressLine: "333 Startup Way, San Francisco, CA 94105"
        });

        receivingParty = Participant({
            name: "FutureInvest Capital Partners",
            role: Party.Receiving,
            addressLine: "777 Investment Drive, New York, NY 10005"
        });

        startDate = 1733952000; // 2025-01-08 in UNIX timestamp
        confidentialityPeriodEnd = 1735728000; // 2028-01-08 in UNIX timestamp
        isActive = true;

        terms.specialTerms.push("Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party");
        terms.terminationConditions.push("Obligations survive termination of discussions");
        terms.terminationConditions.push("Trade Secrets protected for as long as they remain trade secrets under applicable law");
    }

    function addObligation(string memory description, string memory penalty) public onlyReceivingParty {
        obligations.push(Obligation({
            description: description,
            penaltyForBreach: penalty
        }));
        
        emit ObligationAdded(description);
    }

    function finalizeAgreement() public onlyDisclosingParty {
        require(isActive, "Agreement is already finalized or inactive.");
        isActive = false;
        
        emit AgreementFinalized(disclosingParty.name, receivingParty.name);
    }

    function reportBreach(string memory description) public onlyReceivingParty {
        emit BreachReported(receivingParty.name, description);
    }

    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }
}