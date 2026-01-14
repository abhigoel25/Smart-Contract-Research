// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:92:1:
   |
92 | 
   | ^
// This contract failed to compile after 3 fix attempts

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {

    // Parties
    address public lender;
    address public borrower;

    // Financial Terms
    uint public loanAmount;
    uint public monthlyPayment;
    uint public originationFee;

    // Dates
    string public loanDisbursementDate;
    string public firstPaymentDueDate;
    string public loanTermStartDate;

    // Obligations
    struct Obligation {
        string description;
        string deadline;
        string penaltyForBreach;
    }

    Obligation[] public obligations;

    // Termination Conditions
    string[] public terminationConditions;

    // Events
    event LoanDisbursed(address indexed lender, address indexed borrower, uint amount);
    event MonthlyPaymentMade(address indexed borrower, uint amount);
    event ObligationPerformed(address indexed borrower, string description);

    constructor() {
        lender = 0x0; // Default to address(0) for missing data;
        borrower = 0x0; // Default to address(0) for missing data;

        loanAmount = 500000 * 1e18; // Storing amount in wei (assuming 18 decimals)
        monthlyPayment = 9934 * 1e18; // Storing amount in wei (assuming 18 decimals)
        originationFee = 10000 * 1e18; // Storing amount in wei (assuming 18 decimals)

        loanDisbursementDate = "February 1, 2025"; // Default date handling;
        firstPaymentDueDate = "March 1, 2025"; // Default date handling;
        loanTermStartDate = "February 1, 2025"; // Default date handling;

        obligations.push(Obligation("to manage and insure the collateral", "", "default interest rate of 12% per annum"));
        obligations.push(Obligation("to make monthly payments of USD 9,934", "starting March 1, 2025", "5% late payment fee on overdue amount"));

        terminationConditions.push("Default occurs if payment is 15 days late, bankruptcy filing, breach of covenants");
    }

    // Getters
    function getLender() public view returns (address) {
        return lender;
    }

    function getBorrower() public view returns (address) {
        return borrower;
    }

    function getLoanAmount() public view returns (uint) {
        return loanAmount;
    }

    function getMonthlyPayment() public view returns (uint) {
        return monthlyPayment;
    }

    function getOriginationFee() public view returns (uint) {
        return originationFee;
    }

    function getLoanDisbursementDate() public view returns (string memory) {
        return loanDisbursementDate;
    }

    function getFirstPaymentDueDate() public view returns (string memory) {
        return firstPaymentDueDate;
    }

    function getLoanTermStartDate() public view returns (string memory) {
        return loanTermStartDate;
    }

    function getObligation(uint index) public view returns (string memory description, string memory deadline, string memory penalty) {
        require(index < obligations.length, "Invalid obligation index");
        Obligation memory obligation = obligations[index];
        return (obligation.description, obligation.deadline, obligation.penaltyForBreach);