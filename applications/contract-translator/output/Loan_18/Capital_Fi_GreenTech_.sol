// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    struct Party {
        string name;
        string role;
        address addr;  // Store addresses; use address(0) if missing
        string email;
        string entityType;
    }

    struct FinancialTerm {
        uint256 amount;      // Use 0 if missing
        string currency;
        string purpose;
        string frequency;
        string dueDate;      // Use "" if missing
    }

    struct Date {
        string dateType;
        string value;        // Use "" if missing
        uint256 dayOfMonth;  // Use 0 if missing
        string frequency;     // Use "" if missing
    }

    struct Obligation {
        string party;        // "Borrower" or "Lender"
        string description;
        string deadline;      // Use "" if missing
        string penaltyForBreach; // Use "" if missing
    }

    struct Conditions {
        string[] defaultConditions; // Use empty array if missing
        string acceleration;         // Use "" if missing
        uint256 defaultInterestRate; // Use 0 if missing
    }

    Party public lender;
    Party public borrower;
    FinancialTerm public loanTerm;
    FinancialTerm public monthlyPayment;
    Date[] public contractDates;
    Obligation[] public obligations;
    Conditions public conditions;
    string[] public specialTerms;

    event LoanCreated(Party lender, Party borrower, FinancialTerm loanTerm);
    event ObligationMet(string obligationDescription);
    
    constructor() {
        lender = Party({
            name: "Capital Finance Group, LLC",
            role: "lender",
            addr: 0x0000000000000000000000000000000000000000, // Address(0) for missing addresses
            email: "",
            entityType: "company"
        });

        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            addr: 0x0000000000000000000000000000000000000000, // Address(0) for missing addresses
            email: "",
            entityType: "company"
        });
        
        loanTerm = FinancialTerm({
            amount: 500000 ether, // Assuming amount in smallest unit
            currency: "USD",
            purpose: "loan",
            frequency: "one-time",
            dueDate: "February 1, 2025"
        });

        monthlyPayment = FinancialTerm({
            amount: 9934 ether, // Assuming amount in smallest unit
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly",
            dueDate: "March 1, 2025"
        });

        contractDates.push(Date("contract date", "January 10, 2025", 10, ""));
        contractDates.push(Date("disbursement date", "February 1, 2025", 1, ""));
        contractDates.push(Date("first payment due", "March 1, 2025", 1, ""));
        contractDates.push(Date("loan term end", "January 10, 2030", 10, ""));

        obligations.push(Obligation("Borrower", "maintain insurance on collateral at full value", "", ""));
        obligations.push(Obligation("Borrower", "repay loan with specified monthly payments", "March 1, 2025 and monthly thereafter", "5% late payment fee"));
        obligations.push(Obligation("Lender", "hold first security interest in equipment", "", ""));

        conditions = Conditions({
            defaultConditions: ["Payment 15+ days late", "bankruptcy filing", "breach of covenants"],
            acceleration: "Entire remaining balance becomes immediately due",
            defaultInterestRate: 12
        });

        specialTerms.push("Borrower may prepay without penalty");
        specialTerms.push("Early prepayment discounts of 3% if paid within 12 months");

        emit LoanCreated(lender, borrower, loanTerm);
    }

    // View Functions
    function getLender() public view returns (Party memory) {
        return lender;
    }

    function getBorrower() public view returns (Party memory) {
        return borrower;
    }

    function getLoanTerm() public view returns (FinancialTerm memory) {
        return loanTerm;
    }

    function getMonthlyPayment() public view returns (FinancialTerm memory) {
        return monthlyPayment;
    }

    function getContractDate(uint256 index) public view returns (Date memory) {
        if (index < contractDates.length) {
            return contractDates[index];
        } else {
            return Date("", "", 0, ""); // Sensible default if index is invalid
        }
    }

    function getObligation(uint256 index) public view returns (Obligation memory) {
        if (index < obligations.length) {
            return obligations[index];
        } else {
            return Obligation("", "", "", ""); // Sensible default if index is invalid
        }
    }

    function getConditions() public view returns (Conditions memory) {
        return conditions;
    }

    function getSpecialTerms() public view returns (string[] memory) {
        return specialTerms;
    }

    // Action Functions
    function meetObligation(uint256 index) public {
        if (index < obligations.length) {
            emit ObligationMet(obligations[index].description);
        } else {
            // Optional action when index is invalid; silently ignores
        }
    }

    function payLoan() public {
        if (loanTerm.amount > 0) {
            // Logic to process loan payment
        } else {
            // No loan payment to process; gracefully handle without failing
        }
    }

    function payMonthly() public {
        if (monthlyPayment.amount > 0) {
            // Logic to process monthly payment
        } else {
            // No monthly payment to process; gracefully handle without failing
        }
    }
}