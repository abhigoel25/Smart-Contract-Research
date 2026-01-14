// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PromissoryNoteAndLoanAgreement {
    // Parties
    address payable public lender;
    address payable public borrower;

    // Financial terms
    uint256 public loanAmount;
    uint256 public monthlyPayment;
    uint256 public originationFee;
    uint256 public loanStartDate;
    uint256 public loanDisbursementDate;
    uint256 public firstPaymentDueDate;

    // Payment tracking
    uint256 public totalPayments;
    uint256 public paymentsMade;

    // Obligation tracking
    bool public insuranceMaintained;
    bool public loanRepaid;

    // Event logging
    event LoanDisbursed(uint256 amount, uint256 date);
    event PaymentMade(uint256 amount, uint256 date);
    event LoanRepaid(uint256 totalPaid, uint256 date);
    event DefaultOccurred(string reason);

    // Modifiers
    modifier onlyLender() {
        require(msg.sender == lender, "Only lender can call this function");
        _;
    }

    modifier onlyBorrower() {
        require(msg.sender == borrower, "Only borrower can call this function");
        _;
    }

    modifier loanNotRepaid() {
        require(!loanRepaid, "Loan has already been repaid");
        _;
    }

    constructor(address payable _lender, address payable _borrower) {
        lender = _lender;
        borrower = _borrower;

        // Financial terms
        loanAmount = 500000 * 1 ether; // Assuming USD is already converted to equivalent in wei
        monthlyPayment = 9934 * 1 ether; // Assuming USD is already converted to equivalent in wei
        originationFee = 10000 * 1 ether; // Assuming USD is already converted to equivalent in wei

        // Dates
        loanStartDate = 1673203200; // Unix timestamp for January 10, 2025
        loanDisbursementDate = 1675200000; // Unix timestamp for February 1, 2025
        firstPaymentDueDate = 1677628800; // Unix timestamp for March 1, 2025

        totalPayments = loanAmount / monthlyPayment; // Calculate total payments needed
    }

    function disburseLoan() external onlyLender loanNotRepaid {
        require(block.timestamp >= loanDisbursementDate, "Loan cannot be disbursed before due date");
        lender.transfer(loanAmount);
        emit LoanDisbursed(loanAmount, block.timestamp);
    }

    function makePayment() external payable onlyBorrower loanNotRepaid {
        require(msg.value == monthlyPayment, "Incorrect payment amount");
        require(block.timestamp >= firstPaymentDueDate + (30 days * paymentsMade), "Payment is not due yet");

        paymentsMade++;
        emit PaymentMade(msg.value, block.timestamp);

        if (paymentsMade >= totalPayments) {
            loanRepaid = true;
            emit LoanRepaid(msg.value * paymentsMade, block.timestamp);
        }
    }

    function markInsurance(bool status) external onlyBorrower {
        insuranceMaintained = status;
    }

    function checkDefault() external {
        require(block.timestamp >= firstPaymentDueDate + (30 days * paymentsMade), "Payment is not due yet");

        // Logic to check for default
        if (paymentsMade < totalPayments && block.timestamp >= firstPaymentDueDate + (30 days * paymentsMade + 15 days)) {
            emit DefaultOccurred("Payment is 15+ days late");
            loanRepaid = false;
        }
    }

    function terminateContract() external {
        require(!loanRepaid, "Contract cannot be terminated after repayment");
        // Additional logic to handle termination
    }
}