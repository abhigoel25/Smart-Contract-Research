// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    event BreachReported(address indexed party, uint256 penalty);
    event TermEnded(address indexed party);

    address[] public confidentialParties;
    uint public breachPenalty;
    uint public termDays;
    uint public startDate;

    constructor(uint _breachPenalty, uint _termDays) {
        breachPenalty = _breachPenalty;
        termDays = _termDays;
        startDate = block.timestamp;
        
        // Add the parties to the confidential parties list
        confidentialParties.push(0x1234567890123456789012345678901234567890); // InnovateTech Ventures, LLC
        confidentialParties.push(0x0987654321098765432109876543210987654321); // FutureInvest Capital Partners
    }

    function confirmConfidentiality() external {
        // Logic to confirm the confidentiality agreement (stub implementation)
    }

    function reportBreach() external {
        require(isConfidentialParty(msg.sender), "Only confidential parties can report a breach");
        emit BreachReported(msg.sender, breachPenalty);
    }

    function calculatePenalty() external view returns (uint) {
        return breachPenalty;
    }
    
    function isConfidentialParty(address party) internal view returns (bool) {
        for (uint i = 0; i < confidentialParties.length; i++) {
            if (confidentialParties[i] == party) {
                return true;
            }
        }
        return false;
    }

    function checkTermEnd() external {
        require(block.timestamp >= (startDate + (termDays * 1 days)), "Term has not ended yet");
        emit TermEnded(msg.sender);
    }
}