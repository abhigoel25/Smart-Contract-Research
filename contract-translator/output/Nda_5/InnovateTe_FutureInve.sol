// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    address public disclosingParty;
    address public receivingParty;

    enum ObligationStatus { Active, Breached, Completed }
    
    struct Obligation {
        string description;
        ObligationStatus status;
        string penaltyForBreach;
        bool exists;
    }

    struct SpecialTerms {
        string[] terms;
        string conditions;
        string[] terminationConditions;
    }

    mapping(uint => Obligation) public obligations;
    uint public obligationCount;
    
    SpecialTerms public specialTerms;
    
    event ObligationCreated(uint indexed obligationId, string description);
    event ObligationUpdated(uint indexed obligationId, ObligationStatus status);
    event ContractTerminated();
    
    modifier onlyParties() {
        require(msg.sender == disclosingParty || msg.sender == receivingParty, "Not authorized");
        _;
    }

    constructor() {
        disclosingParty = 0xd128d51C475BD1D2b830374F1dC89752E621c805; // InnovateTech Ventures, LLC
        receivingParty = 0xA50A96890CC72c428009E9c1C44A55D1b08aE6B3; // FutureInvest Capital Partners

        // Initializing special terms
        specialTerms.terms.push("Confidentiality Period: 3 years from disclosure date");
        specialTerms.terms.push("Obligations survive termination of discussions");
        specialTerms.terms.push("Trade Secrets protected for as long as they remain trade secrets under applicable law");
        specialTerms.conditions = "Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party";
        
        // Initial obligations
        addObligation("Maintain strict confidentiality, protect information with reasonable security measures", "Breach causes irreparable harm for which monetary damages are inadequate");
        addObligation("Limit disclosure to employees/contractors with need-to-know on confidential basis", "");
        addObligation("Use information only for stated evaluation purposes", "");
        addObligation("Not reverse-engineer or attempt to derive underlying principles", "");
    }

    function addObligation(string memory description, string memory penaltyForBreach) internal {
        obligations[obligationCount] = Obligation({
            description: description,
            status: ObligationStatus.Active,
            penaltyForBreach: penaltyForBreach,
            exists: true
        });
        emit ObligationCreated(obligationCount, description);
        obligationCount++;
    }

    function updateObligationStatus(uint obligationId, ObligationStatus status) external onlyParties {
        require(obligations[obligationId].exists, "Obligation does not exist");
        obligations[obligationId].status = status;
        emit ObligationUpdated(obligationId, status);
    }

    function terminateContract() external onlyParties {
        emit ContractTerminated();
        // Additional termination logic can be implemented here
    }

    function getObligation(uint obligationId) external view returns (string memory description, ObligationStatus status, string memory penaltyForBreach) {
        require(obligations[obligationId].exists, "Obligation does not exist");
        Obligation memory obligation = obligations[obligationId];
        return (obligation.description, obligation.status, obligation.penaltyForBreach);
    }

    function getSpecialTerms() external view returns (string[] memory terms, string memory conditions, string[] memory terminationConditions) {
        return (specialTerms.terms, specialTerms.conditions, specialTerms.terminationConditions);
    }
}