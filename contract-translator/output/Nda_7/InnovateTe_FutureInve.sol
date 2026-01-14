// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    struct Party {
        string name;
        string role;
        string addr;
    }

    struct Obligation {
        string description;
        string penaltyForBreach;
    }

    enum AgreementState { Active, Terminated }

    Party public disclosingParty;
    Party public receivingParty;
    Obligation public obligation;
    AgreementState public state;

    event NDAInitialized(
        address indexed disclosingPartyAddress,
        address indexed receivingPartyAddress,
        uint256 startDate,
        uint256 endDate
    );
    
    event ObligationUpdated(string description, string penaltyForBreach);
    
    event AgreementTerminated(address indexed terminatedBy);
    
    uint256 public startDate;
    uint256 public endDate;

    modifier onlyActive() {
        require(state == AgreementState.Active, "NDA is not active.");
        _;
    }
    
    constructor() {
        disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            role: "Disclosing Party",
            addr: "333 Startup Way, San Francisco, CA 94105"
        });

        receivingParty = Party({
            name: "FutureInvest Capital Partners",
            role: "Receiving Party",
            addr: "777 Investment Drive, New York, NY 10005"
        });

        startDate = 1736217600; // January 8, 2025, in Unix timestamp
        endDate = startDate + (3 * 365 days); // 3 years from disclosure date
        
        obligation = Obligation({
            description: "Maintain strict confidentiality, protect information with reasonable security measures.",
            penaltyForBreach: "Breach causes irreparable harm for which monetary damages are inadequate; entitled to injunctive relief and specific performance."
        });

        state = AgreementState.Active;

        emit NDAInitialized(
            address(this),
            msg.sender,
            startDate,
            endDate
        );
    }
    
    function updateObligation(string memory _description, string memory _penalty) external onlyActive {
        obligation.description = _description;
        obligation.penaltyForBreach = _penalty;

        emit ObligationUpdated(_description, _penalty);
    }

    function terminateAgreement() external onlyActive {
        state = AgreementState.Terminated;

        emit AgreementTerminated(msg.sender);
    }

    function getNDAInfo() external view returns (
        string memory, string memory, string memory,
        string memory, string memory,
        uint256, uint256,
        string memory, string memory
    ) {
        return (
            disclosingParty.name,
            disclosingParty.role,
            disclosingParty.addr,
            receivingParty.name,
            receivingParty.role,
            receivingParty.addr,
            startDate,
            endDate,
            obligation.description,
            obligation.penaltyForBreach
        );
    }
}