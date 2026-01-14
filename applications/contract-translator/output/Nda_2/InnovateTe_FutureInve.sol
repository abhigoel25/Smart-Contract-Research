// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    
    enum Role { DisclosingParty, ReceivingParty }

    struct Party {
        string name;
        Role role;
        string addressLine;
    }

    struct Obligation {
        string description;
        string penaltyForBreach;
    }
    
    struct NDA {
        Party[] parties;
        uint256 startDate;
        uint256 endDate;
        Obligation[] obligations;
        string[] specialTerms;
        string[] terminationConditions;
    }

    NDA public nda;

    event ObligationAdded(string description, string penaltyForBreach);
    event NDAActivated(uint256 startDate, uint256 endDate);
    event NDATerminated();

    address public creator;
    bool public isActive;

    modifier onlyCreator() {
        require(msg.sender == creator, "Only the creator can perform this action");
        _;
    }

    modifier isActiveNDA() {
        require(isActive, "NDA is not active");
        _;
    }

    constructor() {
        creator = msg.sender;
        nda.parties.push(Party("InnovateTech Ventures, LLC", Role.DisclosingParty, "333 Startup Way, San Francisco, CA 94105"));
        nda.parties.push(Party("FutureInvest Capital Partners", Role.ReceivingParty, "777 Investment Drive, New York, NY 10005"));

        nda.startDate = 1736342400; // 2025-01-08
        nda.endDate = 1837857600;   // 2028-01-08

        nda.specialTerms.push("Confidentiality Period: 3 years from disclosure date");
        nda.specialTerms.push("Trade Secrets: Protected for as long as they remain trade secrets under applicable law");
        nda.specialTerms.push("Receiving Party may disclose if required by law/court order with prior written notice");

        nda.terminationConditions.push("Obligations survive termination of discussions");

        isActive = false;
    }

    function activateNDA() external onlyCreator {
        require(!isActive, "NDA is already active");
        isActive = true;
        emit NDAActivated(nda.startDate, nda.endDate);
    }

    function terminateNDA() external onlyCreator isActiveNDA {
        isActive = false;
        emit NDATerminated();
    }

    function addObligation(string calldata description, string calldata penaltyForBreach) external onlyCreator isActiveNDA {
        nda.obligations.push(Obligation(description, penaltyForBreach));
        emit ObligationAdded(description, penaltyForBreach);
    }

    function getObligations() external view isActiveNDA returns (Obligation[] memory) {
        return nda.obligations;
    }

    function getSpecialTerms() external view isActiveNDA returns (string[] memory) {
        return nda.specialTerms;
    }

    function getTerminationConditions() external view isActiveNDA returns (string[] memory) {
        return nda.terminationConditions;
    }
    
}