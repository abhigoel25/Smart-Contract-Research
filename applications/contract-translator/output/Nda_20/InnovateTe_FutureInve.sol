// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {

    struct Party {
        string name;
        string role;
        string addressLine; // Using string type for address for privacy
    }

    struct Date {
        string dateType;
        string value;
        uint dayOfMonth;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Party public disclosingParty;
    Party public receivingParty;
    
    Date public startDate;
    Date public confidentialityEndDate;

    Obligation[] public obligations;

    event AgreementCreated(
        string title,
        string disclosingPartyName,
        string receivingPartyName,
        uint startDate,
        uint confidentialityEndDate
    );

    constructor() {
        // Initialize parties
        disclosingParty = Party("InnovateTech Ventures, LLC", "Disclosing Party", "333 Startup Way, San Francisco, CA 94105");
        receivingParty = Party("FutureInvest Capital Partners", "Receiving Party", "777 Investment Drive, New York, NY 10005");

        // Initialize dates
        startDate = Date("start", "January 8, 2025", 8);
        confidentialityEndDate = Date("confidentiality_period_end", "January 8, 2028", 8);
        
        // Add obligations
        addObligation("Receiving Party", "Maintain strict confidentiality, protect information with reasonable security measures", "", "Breach causes irreparable harm for which monetary damages are inadequate");
        addObligation("Receiving Party", "Limit disclosure to employees/contractors with need-to-know on confidential basis", "", "");
        addObligation("Receiving Party", "Use information only for stated evaluation purposes", "", "");
        addObligation("Receiving Party", "Not reverse-engineer or attempt to derive underlying principles", "", "");

        emit AgreementCreated("MUTUAL NON-DISCLOSURE AGREEMENT", disclosingParty.name, receivingParty.name, block.timestamp, block.timestamp);
    }

    function addObligation(
        string memory party,
        string memory description,
        string memory deadline,
        string memory penaltyForBreach
    ) internal {
        obligations.push(Obligation(party, description, deadline, penaltyForBreach));
    }

    // Getter functions
    function getDisclosingParty() external view returns (string memory name, string memory role, string memory addressLine) {
        return (disclosingParty.name, disclosingParty.role, disclosingParty.addressLine);
    }

    function getReceivingParty() external view returns (string memory name, string memory role, string memory addressLine) {
        return (receivingParty.name, receivingParty.role, receivingParty.addressLine);
    }

    function getStartDate() external view returns (string memory dateType, string memory value, uint dayOfMonth) {
        return (startDate.dateType, startDate.value, startDate.dayOfMonth);
    }

    function getConfidentialityEndDate() external view returns (string memory dateType, string memory value, uint dayOfMonth) {
        return (confidentialityEndDate.dateType, confidentialityEndDate.value, confidentialityEndDate.dayOfMonth);
    }

    function getObligationCount() external view returns (uint count) {
        return obligations.length;
    }

    function getObligation(uint index) external view returns (string memory party, string memory description, string memory deadline, string memory penaltyForBreach) {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            return (obligation.party, obligation.description, obligation.deadline, obligation.penaltyForBreach);
        } else {
            return ("", "", "", ""); // Return defaults for out-of-bounds access
        }
    }
    
    // Add more functions to manage NDA obligations and conditions if needed
}