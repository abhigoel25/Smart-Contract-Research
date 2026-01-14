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
        confidentialParties.push(0x0000000000000000000000000000000000000001); // Disclosing Party
        confidentialParties.push(0x0000000000000000000000000000000000000002); // Receiving Party
    }

    function confirmConfidentiality() public view returns(bool) {
        return true;
    }

    function reportBreach() public {
        emit BreachReported(msg.sender);
    }

    function calculatePenalty() public view returns(uint) {
        return breachPenalty;
    }

    function getConfidentialParties() public view returns(address[] memory) {
        return confidentialParties;
    }

    function getTermDays() public view returns(uint) {
        return termDays;
    }
}