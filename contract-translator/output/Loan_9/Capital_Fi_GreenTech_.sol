// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // State variables for parties
    struct Party {
        string name;
        string role;
        address partyAddress;
        string email;
        string entityType;
    }
    
    Party public lender;
    Party public borrower;

    // Financial terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    FinancialTerm[] public financialTerms;

    // Dates
    struct Date {
        string dateType;
        string value;
        uint256 dayOfMonth;
        string frequency;
    }

    Date[] public importantDates;

    // Obligations
    struct Obligation {
        string party; // "borrower" or "lender"
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Obligation[] public obligations;

    // Conditions
    struct Conditions {
        string[] defaultTriggers;
        string acceleration;
        string defaultInterestRate;
    }

    Conditions public conditions;

    // Events
    event LoanCreated(address indexed lender, address indexed borrower, uint256 amount);
    event ObligationFulfilled(string description);

    // Constructor to initialize the contract
    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            role: "lender",
            partyAddress: address(0), // Missing address
            email: "",
            entityType: "company"
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            partyAddress: address(0), // Missing address
            email: "",
            entityType: "company"
        });
        
        // Initializing financial terms with defaults for missing fields
        financialTerms.push(FinancialTerm({
            amount: 500000,
            currency: "USD",
            purpose: "loan",
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 9.934,
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly",
            dueDate: "March 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 10000,
            currency: "USD",
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: ""
        }));

        importantDates.push(Date({
            dateType: "loan_disbursement",
            value: "February 1, 2025",
            dayOfMonth: 1,
            frequency: ""
        }));
        
        importantDates.push(Date({
            dateType: "first_payment_due",
            value: "March 1, 2025",
            dayOfMonth: 1,
            frequency: ""
        }));

        obligations.push(Obligation({
            party: "borrower",
            description: "maintain insurance on collateral at full value",
            deadline: "",
            penaltyForBreach: ""
        }));

        conditions = Conditions({
            defaultTriggers: new string[](3),
            acceleration: "Entire remaining balance becomes immediately due",
            defaultInterestRate: "12% per annum on unpaid balance"
        });

        conditions.defaultTriggers[0] = "Payment 15+ days late";
        conditions.defaultTriggers[1] = "bankruptcy filing";
        conditions.defaultTriggers[2] = "breach of covenants";

        emit LoanCreated(lender.partyAddress, borrower.partyAddress, 500000);
    }

    // Getter functions
    function getLender() public view returns (string memory, string memory, address, string memory, string memory) {
        return (lender.name, lender.role, lender.partyAddress, lender.email, lender.entityType);
    }

    function getBorrower() public view returns (string memory, string memory, address, string memory, string memory) {
        return (borrower.name, borrower.role, borrower.partyAddress, borrower.email, borrower.entityType);
    }

    function getFinancialTerms(uint256 index) public view returns (uint256, string memory, string memory, string memory, string memory) {
        if (index >= financialTerms.length) return (0, "", "", "", ""); // Out of bounds check
        FinancialTerm memory term = financialTerms[index];
        return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
    }

    function getImportantDate(uint256 index) public view returns (string memory, string memory, uint256, string memory) {
        if (index >= importantDates.length) return ("", "", 0, ""); // Out of bounds check
        Date memory date = importantDates[index];
        return (date.dateType, date.value, date.dayOfMonth, date.frequency);
    }
    
    function getObligation(uint256 index) public view returns (string memory, string memory, string memory, string memory) {
        if (index >= obligations.length) return ("", "", "", ""); // Out of bounds check
        Obligation memory obligation = obligations[index];
        return (obligation.party, obligation.description, obligation.deadline, obligation.penaltyForBreach);
    }

    // Action functions
    function fulfillObligation(uint256 index) public {
        if (index < obligations.length) {
            // Just emitting event, simulating the fulfillment of the obligation
            emit ObligationFulfilled(obligations[index].description);
        }
    }

    function checkLoanAmount() public view returns (bool) {
        return financialTerms[0].amount > 0; // Check if loan amount is greater than 0
    }

    function calculateDefaultInterest(uint256 unpaidAmount) public view returns (uint256) {
        if (unpaidAmount > 0) {
            // Simple interest calculation assuming the rate can be applied
            uint256 interest = (unpaidAmount * 12) / 100; // 12% interest rate
            return interest;
        } else {
            return 0; // No unpaid amount
        }
    }
}