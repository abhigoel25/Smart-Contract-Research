// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    struct Party {
        string name;
        address addr;
    }

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string due_date;
    }

    struct Date {
        string date_type;
        string value;
        uint256 day_of_month;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penalty_for_breach;
    }

    Party public lender;
    Party public borrower;

    FinancialTerm[] public financialTerms;

    Date[] public dates;

    Obligation[] public obligations;

    event LoanCreated(address lender, address borrower, uint256 loanAmount);
    event PaymentMade(address borrower, uint256 amount);

    constructor() {
        lender = Party("Capital Finance Group, LLC", 0x5555555555555555555555555555555555555555); // Placeholder address, use accurate one
        borrower = Party("GreenTech Solutions, Inc.", address(0)); // address(0) since missing

        // Initialize financial terms
        financialTerms.push(FinancialTerm(500000, "USD", "loan", "one-time", "February 1, 2025"));
        financialTerms.push(FinancialTerm(9934, "USD", "monthly payment", "monthly", "March 1, 2025"));
        financialTerms.push(FinancialTerm(10000, "USD", "origination fee", "one-time", ""));
        financialTerms.push(FinancialTerm(0, "USD", "late payment fee", "per occurrence", ""));

        // Initialize dates
        dates.push(Date("loan_disbursement", "February 1, 2025", 1, ""));
        dates.push(Date("first_payment_due", "March 1, 2025", 1, "monthly"));
        dates.push(Date("contract_start", "January 10, 2025", 10, ""));
        
        // Initialize obligations
        obligations.push(Obligation("borrower", "maintain insurance on collateral at full value", "", ""));
        obligations.push(Obligation("borrower", "payments due monthly as per repayment schedule", "monthly starting March 1, 2025", "5% late payment fee on overdue amount"));
        obligations.push(Obligation("lender", "provide loan amount on disbursement date", "February 1, 2025", ""));
        
        emit LoanCreated(lender.addr, borrower.addr, financialTerms[0].amount);
    }

    // Getters for Parties
    function getLender() public view returns (string memory name, address addr) {
        return (lender.name, lender.addr);
    }

    function getBorrower() public view returns (string memory name, address addr) {
        return (borrower.name, borrower.addr);
    }

    // Getters for Financial Terms
    function getFinancialTerm(uint index) public view returns (uint256 amount, string memory currency, string memory purpose, string memory frequency, string memory due_date) {
        if (index < financialTerms.length) {
            FinancialTerm memory term = financialTerms[index];
            return (term.amount, term.currency, term.purpose, term.frequency, term.due_date);
        }
        return (0, "", "", "", "");
    }

    // Getters for Dates
    function getDate(uint index) public view returns (string memory date_type, string memory value, uint256 day_of_month, string memory frequency) {
        if (index < dates.length) {
            Date memory date = dates[index];
            return (date.date_type, date.value, date.day_of_month, date.frequency);
        }
        return ("", "", 0, "");
    }

    // Getters for Obligations
    function getObligation(uint index) public view returns (string memory party, string memory description, string memory deadline, string memory penalty) {
        if (index < obligations.length) {
            Obligation memory obligation = obligations[index];
            return (obligation.party, obligation.description, obligation.deadline, obligation.penalty_for_breach);
        }
        return ("", "", "", "");
    }

    // Action Function: Acknowledges the borrower's obligation
    function acknowledgeObligation(uint index) public {
        if (index < obligations.length - 1) {
            // Perform the action only if it's a valid obligation and amounts are valid
            // Optional conditions can be checked here
        }
    }

    // Action Function: Handle a payment made by borrower
    function makePayment(uint256 paymentAmount) public {
        if (paymentAmount > 0 && paymentAmount <= financialTerms[1].amount) {
            emit PaymentMade(borrower.addr, paymentAmount);
            // Process the payment
        }
    }
}