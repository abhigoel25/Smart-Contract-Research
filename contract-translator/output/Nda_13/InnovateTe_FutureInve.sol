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
        confidentialParties.push(msg.sender); // Adding the contract deployer as a confidential party
    }

    function confirmConfidentiality(address _party) public {
        confidentialParties.push(_party);
    }

    function reportBreach() public {
        emit BreachReported(msg.sender);
    }

    function calculatePenalty() public view returns (uint) {
        return breachPenalty;
    }
}