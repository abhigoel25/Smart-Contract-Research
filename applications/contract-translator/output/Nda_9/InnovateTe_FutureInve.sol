// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    event BreachReported(address indexed party);
    event TermEnded();

    address[] public confidentialParties;
    uint public breachPenalty;
    uint public termDays;

    constructor(uint _breachPenalty, uint _termDays) {
        breachPenalty = _breachPenalty;
        termDays = _termDays;
        confidentialParties.push(0x1234567890abcdef1234567890abcdef12345678); // Disclosing Party
        confidentialParties.push(0xabcdef1234567890abcdef1234567890abcdef12); // Receiving Party
    }

    function confirmConfidentiality() external view returns (bool) {
        return true;
    }

    function reportBreach() external {
        emit BreachReported(msg.sender);
    }

    function calculatePenalty() external view returns (uint) {
        return breachPenalty;
    }

    function getConfidentialParties() external view returns (address[] memory) {
        return confidentialParties;
    }
}