// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    // State variables
    address public disclosingPartyAddress;
    address public receivingPartyAddress;

    string public disclosingPartyName;
    string public receivingPartyName;

    uint256 public startDate;
    uint256 public endDate;

    struct Obligation {
        string party;
        string description;
        string penaltyForBreach;
    }

    Obligation[] public obligations;
    
    string[] public specialTerms;
    string[] public terminationConditions;

    // Events
    event ObligationCreated(string party, string description);
    event SpecialTermAdded(string term);
    event TerminationConditionAdded(string condition);

    // Constructor
    constructor() {
        disclosingPartyName = "InnovateTech Ventures, LLC";
        receivingPartyName = "FutureInvest Capital Partners";

        disclosingPartyAddress = address(0);
        receivingPartyAddress = address(0);

        startDate = 1704672000; // January 8, 2025 (timestamp)
        endDate = 1736208000;   // January 8, 2028 (timestamp)

        obligations.push(Obligation({
            party: "Receiving Party",
            description: "Maintain strict confidentiality, protect information with reasonable security measures, limit disclosure to employees/contractors with need-to-know, use information only for stated evaluation purposes, not reverse-engineer or attempt to derive underlying principles",
            penaltyForBreach: "Breach causes irreparable harm for which monetary damages are inadequate, entitled to injunctive relief and specific performance"
        }));
        
        specialTerms.push("Confidential information includes technical data, source code, algorithms, business plans, financial projections, customer lists, trade secrets, proprietary methodologies, software, specifications, and know-how");
        specialTerms.push("Exclusions include public domain information, independently developed information, rightfully received from third parties");
        specialTerms.push("Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party when legally permitted");
        
        terminationConditions.push("Obligations survive termination of discussions");
        terminationConditions.push("Trade secrets protected for as long as they remain trade secrets under applicable law");
    }

    // Getter functions
    function getDisclosingParty() public view returns (string memory, address) {
        return (disclosingPartyName, disclosingPartyAddress);
    }

    function getReceivingParty() public view returns (string memory, address) {
        return (receivingPartyName, receivingPartyAddress);
    }

    function getStartDate() public view returns (uint256) {
        return startDate;
    }

    function getEndDate() public view returns (uint256) {
        return endDate;
    }

    function getObligation(uint256 index) public view returns (string memory, string memory, string memory) {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            return (obligation.party, obligation.description, obligation.penaltyForBreach);
        } else {
            return ("", "", ""); // Return default values
        }
    }

    function getObligationCount() public view returns (uint256) {
        return obligations.length;
    }

    function getSpecialTerm(uint256 index) public view returns (string memory) {
        if (index < specialTerms.length) {
            return specialTerms[index];
        } else {
            return ""; // Return default value
        }
    }

    function getSpecialTermCount() public view returns (uint256) {
        return specialTerms.length;
    }

    function getTerminationCondition(uint256 index) public view returns (string memory) {
        if (index < terminationConditions.length) {
            return terminationConditions[index];
        } else {
            return ""; // Return default value
        }
    }

    function getTerminationConditionCount() public view returns (uint256) {
        return terminationConditions.length;
    }

    // Action functions
    function createObligation(string memory _party, string memory _description, string memory _penaltyForBreach) public {
        // Allow adding obligations regardless of optional fields
        obligations.push(Obligation({
            party: _party,
            description: _description,
            penaltyForBreach: _penaltyForBreach
        }));
        emit ObligationCreated(_party, _description);
    }

    function addSpecialTerm(string memory term) public {
        specialTerms.push(term);
        emit SpecialTermAdded(term);
    }

    function addTerminationCondition(string memory condition) public {
        terminationConditions.push(condition);
        emit TerminationConditionAdded(condition);
    }
}