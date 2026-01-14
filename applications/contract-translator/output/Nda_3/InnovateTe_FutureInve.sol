// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    address private disclosingParty;
    address private receivingParty;
    
    struct Dates {
        uint256 startDate;
        uint256 confidentialityPeriodEnd;
    }

    Dates public ndaDates;

    struct Obligation {
        string description;
        string penaltyForBreach;
    }

    Obligation public obligation;

    // Events
    event AgreementCreated(address indexed disclosingParty, address indexed receivingParty, uint256 startDate, uint256 confidentialityPeriodEnd);
    event ObligationUpdated(string description, string penaltyForBreach);
    event ConfidentialityBreached(address indexed party, string details);

    // Modifier to check if the caller is either party
    modifier onlyParties() {
        require(msg.sender == disclosingParty || msg.sender == receivingParty, "Not authorized.");
        _;
    }

    constructor() {
        disclosingParty = 0x1D2A3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0C; // Replace with actual address
        receivingParty = 0xA1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0; // Replace with actual address
        ndaDates.startDate = 1736377200; // Timestamp for 2025-01-08
        ndaDates.confidentialityPeriodEnd = 1736377200 + 3 * 365 days; // Until 2028-01-08
        obligation.description = "Maintain strict confidentiality; protect information with reasonable security measures; limit disclosure to employees/contractors with need-to-know; use information only for stated evaluation purposes; not reverse-engineer or attempt to derive underlying principles.";
        obligation.penaltyForBreach = "Breach causes irreparable harm for which monetary damages are inadequate.";
        emit AgreementCreated(disclosingParty, receivingParty, ndaDates.startDate, ndaDates.confidentialityPeriodEnd);
    }

    function updateObligation(string memory _description, string memory _penaltyForBreach) external onlyParties {
        obligation.description = _description;
        obligation.penaltyForBreach = _penaltyForBreach;
        emit ObligationUpdated(_description, _penaltyForBreach);
    }

    function reportConfidentialityBreach(string memory details) external onlyParties {
        emit ConfidentialityBreached(msg.sender, details);
    }

    function getNdaDetails() external view returns (address, address, Dates memory, Obligation memory) {
        return (disclosingParty, receivingParty, ndaDates, obligation);
    }
}