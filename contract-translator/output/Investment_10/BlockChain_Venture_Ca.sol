// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SeriesAPreferredStockPurchaseAgreement {
    
    // State Variables
    struct Party {
        string name;
        string role;
        address addr;
        string email;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        uint256 dueDate; // Unix timestamp for the due date
    }
    
    struct DateInfo {
        string dateType;
        string value; // Date as string (ISO format)
        uint256 dayOfMonth;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Party[2] public parties; // 0: Company, 1: Investor
    FinancialTerm[2] public financialTerms;
    DateInfo[2] public dates;
    Obligation[2] public obligations;

    // Events
    event InvestmentExecuted(uint256 investmentAmount);
    event ObligationFulfilled(string party, string description);

    // Constructor to initialize the contract
    constructor() {
        // Initializing parties with default values
        parties[0] = Party("BlockChain Innovations Inc.", "Company", address(0), "", "company");
        parties[1] = Party("Venture Capital Fund VII, LP", "Investor", address(0), "", "company");

        // Initializing financial terms with provided values
        financialTerms[0] = FinancialTerm(8000000, "USD", "purchase price per share", "one-time", 0);
        financialTerms[1] = FinancialTerm(10000000, "USD", "total investment amount", "one-time", 0);

        // Initializing dates with provided values
        dates[0] = DateInfo("start", "2025-01-01", 1, "");
        dates[1] = DateInfo("redemption_trigger", "2030-01-01", 1, "");

        // Initializing obligations
        obligations[0] = Obligation("Company", "Redeem shares if no qualified IPO by redemption trigger date.", "12 months from redemption trigger event", "");
        obligations[1] = Obligation("Investor", "Must participate in company sale if approved by majority holders.", "upon company sale event", "");
    }

    // Getters
    function getParty(uint8 index) public view returns (string memory name, string memory role, address addr, string memory email, string memory entityType) {
        if (index < 2) {
            Party memory party = parties[index];
            return (party.name, party.role, party.addr, party.email, party.entityType);
        } else {
            return ("", "", address(0), "", "");
        }
    }

    function getFinancialTerm(uint8 index) public view returns (uint256 amount, string memory currency, string memory purpose, string memory frequency, uint256 dueDate) {
        if (index < 2) {
            FinancialTerm memory term = financialTerms[index];
            return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
        } else {
            return (0, "", "", "", 0);
        }
    }

    function getDateInfo(uint8 index) public view returns (string memory dateType, string memory value, uint256 dayOfMonth, string memory frequency) {
        if (index < 2) {
            DateInfo memory dateInfo = dates[index];
            return (dateInfo.dateType, dateInfo.value, dateInfo.dayOfMonth, dateInfo.frequency);
        } else {
            return ("", "", 0, "");
        }
    }

    function fulfillObligation(uint8 index) public {
        require(index < 2, "Invalid obligation index");
        
        Obligation memory obligation = obligations[index];

        // Only execute if there's a relevant obligation
        if (bytes(obligation.description).length > 0) {
            emit ObligationFulfilled(obligation.party, obligation.description);
        }
    }

    function executeInvestment() public {
        uint256 totalInvestmentAmount = financialTerms[1].amount;

        // Check if the total investment amount is greater than zero
        if (totalInvestmentAmount > 0) {
            emit InvestmentExecuted(totalInvestmentAmount);
            // Here you would typically handle transferring the investment amount in a real contract
        }
    }
}