// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {
    
    enum Role { DisclosingParty, ReceivingParty }
    
    struct Party {
        string name;
        string entityType;
        string addressLine;
    }

    struct Obligation {
        string description;
        bool isMet;
    }
    
    struct NDA {
        Party disclosingParty;
        Party receivingParty;
        uint256 startDate;
        uint256 endDate;
        Obligation[] obligations;
        string conditions;
        string terminationConditions;
        event NDAEvent(string message);
    }

    NDA public nda;

    modifier onlyReceivingParty() {
        require(msg.sender == address(this), "Only the receiving party can perform this action");
        _;
    }

    constructor() {
        nda.disclosingParty = Party({
            name: "InnovateTech Ventures, LLC",
            entityType: "company",
            addressLine: "333 Startup Way, San Francisco, CA 94105"
        });

        nda.receivingParty = Party({
            name: "FutureInvest Capital Partners",
            entityType: "company",
            addressLine: "777 Investment Drive, New York, NY 10005"
        });

        nda.startDate = 1736035200; // January 8, 2025
        nda.endDate = nda.startDate + 3 * 365 days; // 3 years from the start date
        
        nda.obligations.push(Obligation({
            description: "Maintain strict confidentiality, protect information with reasonable security measures",
            isMet: false
        }));
        nda.obligations.push(Obligation({
            description: "Limit disclosure to employees/contractors with need-to-know on confidential basis",
            isMet: false
        }));
        nda.obligations.push(Obligation({
            description: "Use information only for stated evaluation purposes",
            isMet: false
        }));
        nda.obligations.push(Obligation({
            description: "Not reverse-engineer or attempt to derive underlying principles",
            isMet: false
        }));
        
        nda.conditions = "Receiving Party may disclose if required by law/court order, prior written notice to Disclosing Party required when legally permitted.";
        nda.terminationConditions = "Obligations survive termination of discussions.";

        emit NDAEvent("NDA created successfully");
    }

    function fulfillObligation(uint256 obligationIndex) external onlyReceivingParty {
        require(obligationIndex < nda.obligations.length, "Invalid obligation index");
        nda.obligations[obligationIndex].isMet = true;

        emit NDAEvent(string(abi.encodePacked("Obligation fulfilled: ", nda.obligations[obligationIndex].description)));
    }

    function getNDAData() external view returns (
        string memory disclosingPartyName, 
        string memory disclosingPartyAddress, 
        string memory receivingPartyName, 
        string memory receivingPartyAddress, 
        uint256 startDate, 
        uint256 endDate, 
        Obligation[] memory obligations, 
        string memory conditions, 
        string memory terminationConditions
    ) {
        return (
            nda.disclosingParty.name,
            nda.disclosingParty.addressLine,
            nda.receivingParty.name,
            nda.receivingParty.addressLine,
            nda.startDate,
            nda.endDate,
            nda.obligations,
            nda.conditions,
            nda.terminationConditions
        );
    }
}