// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {

    struct Party {
        string name;
        string role; // Disclosing Party or Receiving Party
        string addr; // Address
        string entityType; // Company or individual
    }

    struct Obligation {
        string party; // Indicate which party has the obligation
        string description; // Obligation description
        string penaltyForBreach; // Penalty for breach
    }

    struct Term {
        uint256 startDate; // Start date as a timestamp
        uint256 endDate; // End date as a timestamp
    }

    struct SpecialTerm {
        string description;
    }

    // State variables
    Party public disclosingParty;
    Party public receivingParty;
    Term public term;
    Obligation[] public obligations;
    SpecialTerm[] public specialTerms;
    string public conditions;

    event ObligationLogged(string party, string description, string penalty);
    event SpecialTermAdded(string description);

    modifier onlyReceivingParty() {
        require(
            msg.sender == address(this),
            "Only Receiving Party can call this function"
        );
        _;
    }

    constructor() {
        disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            role: "Disclosing Party",
            addr: "333 Startup Way, San Francisco, CA 94105",
            entityType: "company"
        });

        receivingParty = Party({
            name: "FutureInvest Capital Partners",
            role: "Receiving Party",
            addr: "777 Investment Drive, New York, NY 10005",
            entityType: "company"
        });

        term = Term({
            startDate: 1736409600, // January 8, 2025
            endDate: 1767945600  // January 8, 2028
        });

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Maintain strict confidentiality and protect information with reasonable security measures.",
            penaltyForBreach: "Breach causes irreparable harm; entitled to injunctive relief and specific performance."
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Limit disclosure to employees/contractors with a need-to-know on a confidential basis.",
            penaltyForBreach: ""
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Use information only for stated evaluation purposes.",
            penaltyForBreach: ""
        }));

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Not reverse-engineer or attempt to derive underlying principles.",
            penaltyForBreach: ""
        }));

        specialTerms.push(SpecialTerm({
            description: "Confidential Information excludes public domain information, independently developed information, and information rightfully received from third parties."
        }));

        specialTerms.push(SpecialTerm({
            description: "Confidentiality obligations survive termination of discussions."
        }));

        specialTerms.push(SpecialTerm({
            description: "Trade secrets are protected for as long as they remain trade secrets under applicable law."
        }));

        conditions = "Receiving Party may disclose if required by law/court order, with prior written notice to Disclosing Party required when legally permitted.";
    }

    function logObligation(string calldata _party, string calldata _description, string calldata _penalty) external onlyReceivingParty {
        obligations.push(Obligation({
            party: _party,
            description: _description,
            penaltyForBreach: _penalty
        }));

        emit ObligationLogged(_party, _description, _penalty);
    }

    function addSpecialTerm(string calldata _description) external onlyReceivingParty {
        specialTerms.push(SpecialTerm({
            description: _description
        }));

        emit SpecialTermAdded(_description);
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function getSpecialTerms() external view returns (SpecialTerm[] memory) {
        return specialTerms;
    }

    function getPartiesInfo() external view returns (Party memory, Party memory) {
        return (disclosingParty, receivingParty);
    }

    function getTerm() external view returns (Term memory) {
        return term;
    }
}