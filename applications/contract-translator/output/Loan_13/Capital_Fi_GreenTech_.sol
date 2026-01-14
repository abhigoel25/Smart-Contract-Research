// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    struct Party {
        string name;
        string role;
        address addr; // Use 0 address if not provided
    }

    struct FinancialTerm {
        uint256 amount; // Use 0 if not provided
        string currency;
        string purpose;
        string frequency;
        string dueDate; // Use "" if not provided
    }

    struct DateInfo {
        string dateType;
        string value; // Use "" if not provided
        uint256 dayOfMonth; // Use 0 if not provided
        string frequency; // Use "" if not provided
    }

    struct Obligation {
        string party; // Represented by "borrower" or "lender"
        string description;
        string deadline;
        string penaltyForBreach; // Use "" if not provided
    }

    struct Condition {
        string[] defaultTriggers; // Use empty array if not provided
        string defaultInterestRate; // Use "" if not provided
    }

    Party public lender;
    Party public borrower;
    FinancialTerm[] public financialTerms;
    DateInfo[] public dates;
    Obligation[] public obligations;
    Condition public conditions;

    event LoanCreated(address indexed lender, address indexed borrower);
    event PaymentMade(uint256 amount);
    event ObligationFulfilled(string obligationDescription);

    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            role: "lender",
            addr: 0x0000000000000000000000000000000000000000 // Use address(0) for missing address
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            addr: 0x0000000000000000000000000000000000000000 // Use address(0) for missing address
        });

        // Financial terms
        financialTerms.push(FinancialTerm({
            amount: 500000,
            currency: "USD",
            purpose: "loan",
            frequency: "one-time",
            dueDate: "February 1, 2025"
        }));

        financialTerms.push(FinancialTerm({
            amount: 10000,
            currency: "USD",
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: "at loan disbursement"
        }));

        financialTerms.push(FinancialTerm({
            amount: 9934,
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly",
            dueDate: "March 1, 2025"
        }));

        // Dates
        dates.push(DateInfo({
            dateType: "start",
            value: "January 10, 2025",
            dayOfMonth: 10,
            frequency: "" // Use empty if not provided
        }));
        
        dates.push(DateInfo({
            dateType: "disbursement",
            value: "February 1, 2025",
            dayOfMonth: 1,
            frequency: "" // Use empty if not provided
        }));

        dates.push(DateInfo({
            dateType: "first_payment_due",
            value: "March 1, 2025",
            dayOfMonth: 1,
            frequency: "monthly"
        }));

        dates.push(DateInfo({
            dateType: "term_end",
            value: "January 10, 2030",
            dayOfMonth: 10,
            frequency: "annual"
        }));

        // Obligations
        obligations.push(Obligation({
            party: "borrower",
            description: "repay the loan amount including interest",
            deadline: "monthly for 5 years",
            penaltyForBreach: "5% late payment fee; acceleration of entire remaining balance"
        }));

        obligations.push(Obligation({
            party: "borrower",
            description: "maintain insurance on collateral at full value",
            deadline: "ongoing",
            penaltyForBreach: "" // Use empty if not provided
        }));

        // Conditions
        conditions = Condition({
            defaultTriggers: new string[](0), // Empty array as a default
            defaultInterestRate: "12% per annum on unpaid balance"
        });

        emit LoanCreated(lender.addr, borrower.addr);
    }

    // Getters
    function getLender() public view returns (string memory, string memory, address) {
        return (lender.name, lender.role, lender.addr);
    }

    function getBorrower() public view returns (string memory, string memory, address) {
        return (borrower.name, borrower.role, borrower.addr);
    }

    function getFinancialTerm(uint256 index) public view returns (uint256, string memory, string memory, string memory, string memory) {
        if (index >= financialTerms.length) {
            return (0, "", "", "", "");
        }
        FinancialTerm memory term = financialTerms[index];
        return (term.amount, term.currency, term.purpose, term.frequency, term.dueDate);
    }

    function getDateInfo(uint256 index) public view returns (string memory, string memory, uint256, string memory) {
        if (index >= dates.length) {
            return ("", "", 0, "");
        }
        DateInfo memory dateInfo = dates[index];
        return (dateInfo.dateType, dateInfo.value, dateInfo.dayOfMonth, dateInfo.frequency);
    }

    function getObligation(uint256 index) public view returns (string memory, string memory, string memory, string memory) {
        if (index >= obligations.length) {
            return ("", "", "", "");
        }
        Obligation memory obligation = obligations[index];
        return (obligation.party, obligation.description, obligation.deadline, obligation.penaltyForBreach);
    }

    function getDefaultInterestRate() public view returns (string memory) {
        return conditions.defaultInterestRate;
    }

    // Action functions
    function makePayment(uint256 amount) public {
        if (amount > 0) {
            emit PaymentMade(amount);
        }
    }

    function fulfillObligation(uint256 index) public {
        if (index < obligations.length) {
            emit ObligationFulfilled(obligations[index].description);
        }
    }

    // More functionality can be added here
}