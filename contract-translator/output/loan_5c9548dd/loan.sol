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
            role: "lender",
            addr: 0x0000000000000000000000000000000000000000 // Assuming address is missing
        });

        // Initialize borrower
        borrower = Party({
            name: "GreenTech Solutions, Inc.",
            role: "borrower",
            addr: 0x0000000000000000000000000000000000000000 // Assuming address is missing
        });
        
        // Initialize loan
        loan = FinancialTerm({
            amount: 500000,
            currency: "USD",
            purpose: "loan",
            frequency: "one-time",
            dueDate: "February 1, 2025"
        });

        // Initialize monthly payment
        monthlyPayment = FinancialTerm({
            amount: 9934,
            currency: "USD",
            purpose: "monthly payment",
            frequency: "monthly",
            dueDate: "starting March 1, 2025"
        });

        // Initialize origination fee
        originationFee = FinancialTerm({
            amount: 10000,
            currency: "USD",
            purpose: "origination fee",
            frequency: "one-time",
            dueDate: ""
        });
        
        // Initialize dates
        executionDate = Date({
            dateType: "execution",
            value: "January 10, 2025",
            dayOfMonth: 10
        });

        disbursementDate = Date({
            dateType: "disbursement",
            value: "February 1, 2025",
            dayOfMonth: 1
        });

        firstPaymentDueDate = Date({
            dateType: "first_payment_due",
            value: "March 1, 2025",
            dayOfMonth: 1
        });

        // Initialize obligations
        obligations.push(Obligation({
            party: "Borrower",
            description: "Maintain insurance on collateral at full value",
            deadline: ""
        }));

        obligations.push(Obligation({
            party: "Lender",
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
    }

    function getBorrower() public view returns (string memory, string memory, address) {
        return (borrower.name, borrower.role, borrower.addr);
    }

    function getLoanDetails() public view returns (uint256, string memory, string memory, string memory, string memory) {
        return (loan.amount, loan.currency, loan.purpose, loan.frequency, loan.dueDate);
    }

    function getMonthlyPaymentDetails() public view returns (uint256, string memory, string memory, string memory, string memory) {
        return (monthlyPayment.amount, monthlyPayment.currency, monthlyPayment.purpose, monthlyPayment.frequency, monthlyPayment.dueDate);
    }

    function getOriginationFeeDetails() public view returns (uint256, string memory, string memory, string memory, string memory) {
        return (originationFee.amount, originationFee.currency, originationFee.purpose, originationFee.frequency, originationFee.dueDate);
    }

    function getExecutionDate() public view returns (string memory, uint256) {
        return (executionDate.value, executionDate.dayOfMonth);
    }

    function getDisbursementDate() public view returns (string memory, uint256) {
        return (disbursementDate.value, disbursementDate.dayOfMonth);
    }

    function getFirstPaymentDueDate() public view returns (string memory, uint256) {
        return (firstPaymentDueDate.value, firstPaymentDueDate.dayOfMonth);
    }

    function getObligationCount() public view returns (uint256) {
        return obligations.length;
    }

    function getObligation(uint256 index) public view returns (string memory, string memory, string memory) {
        if (index < obligations.length) {
            return (obligations[index].party, obligations[index].description, obligations[index].deadline);
        } else {
            return ("", "", ""); // Return empty values if index is out of bounds
        }
    }

    function getSpecialTerms() public view returns (string[] memory) {
        return specialTerms;
    }

    function getTerminationConditions() public view returns (string[] memory) {
        return terminationConditions;
    }

    // Action functions
    function performLoanDisbursement() public {
        if (loan.amount > 0) {
            // Logic to disburse the loan
            emit LoanDisbursed(loan.amount, loan.currency);
        }
    }

    function makePayment(uint256 amount) public {
        if (amount > 0) {
            // Logic for making a payment
            emit PaymentMade(amount, monthlyPayment.currency);
        }
    }
}