// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected ',' but got ';'
  --> <stdin>:72:61:
   |
72 |             addr: 0x0000000000000000000000000000000000000000; // Assuming address is missing
   |                                                             ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    // Parties
    struct Party {
        string name;
        string role;
        address addr;
    }

    Party public lender;
    Party public borrower;

    // Financial Terms
    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    FinancialTerm public loan;
    FinancialTerm public monthlyPayment;
    FinancialTerm public originationFee;

    // Dates
    struct Date {
        string dateType;
        string value;
        uint256 dayOfMonth;
    }

    Date public executionDate;
    Date public disbursementDate;
    Date public firstPaymentDueDate;

    // Obligations
    struct Obligation {
        string party;
        string description;
        string deadline;
    }

    Obligation[] public obligations;

    // Special Terms
    string[] public specialTerms;

    // Conditions
    struct Conditions {
        string[] defaultTriggers;
        string acceleration;
        string defaultInterestRate;
    }

    Conditions public conditions;

    // Termination Conditions
    string[] public terminationConditions;

    // Events
    event LoanDisbursed(uint256 amount, string currency);
    event PaymentMade(uint256 amount, string currency);

    // Constructor
    constructor() {
        // Initialize lender
        lender = Party({
            name: "Capital Finance Group, LLC",
            addr: 0x0000000000000000000000000000000000000000; // Assuming address is missing
        });

        // Initialize borrower
        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            addr: 0x0000000000000000000000000000000000000000; // Assuming address is missing
        });

        // Initialize loan
        loan = FinancialTerm({
            frequency: "one-time",
            dueDate: "February 1, 2025"
        });

        // Initialize monthly payment
        monthlyPayment = FinancialTerm({
            purpose: "monthly payment",
            dueDate: "starting March 1, 2025"
        });

        // Initialize origination fee
        originationFee = FinancialTerm({
            purpose: "origination fee",
            frequency: "one-time",
        });

        // Initialize dates
        executionDate = Date({
            value: "January 10, 2025",
        });

        disbursementDate = Date({
            value: "February 1, 2025",
        });

        firstPaymentDueDate = Date({
            value: "March 1, 2025",
        });

        // Initialize obligations
        obligations.push(Obligation({
            description: "Maintain insurance on collateral at full value",
        }));

        obligations.push(Obligation({
            description: "Provide loan amount as stated",
            deadline: "February 1, 2025"
        }));

        // Special terms
        specialTerms.push("Borrower may prepay without penalty");
        specialTerms.push("3% early prepayment discount if paid within 12 months");

        // Conditions
        conditions.defaultTriggers = ["Payment 15+ days late", "Bankruptcy filing", "Breach of covenants"];
        conditions.acceleration = "Entire remaining balance becomes immediately due";
        conditions.defaultInterestRate = "12% per annum on unpaid balance";

        // Termination conditions
        terminationConditions.push("In case of default as defined");
    }

    // View functions with sensible defaults
    function getLender() public view returns (string memory, string memory, address) {
        return (lender.name, lender.role, lender.addr);