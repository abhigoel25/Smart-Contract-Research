// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PromissoryNoteAndLoanAgreement {
    address public lender;
    address public borrower;
    
    uint256 public loanAmount;
    uint256 public monthlyPayment;
    uint256 public originationFee;
    
    uint256 public loanStartDate;
    uint256 public disbursementDate;
    uint256 public firstPaymentDueDate;
    uint256 public loanTermEndDate;
    
    bool public loanDisbursed;
    bool public loanDefaulted;
    
    uint256 public remainingBalance;
    
    event LoanDisbursed(uint256 amount, uint256 disbursementDate);
    event PaymentMade(uint256 amount, uint256 paymentDate);
    event LoanDefaulted(string reason);
    event ObligationsUpdated(string obligation);
    
    constructor(address _borrower) {
        lender = msg.sender;
        borrower = _borrower;
        
        loanAmount = 500000 ether; // Loan amount in wei
        monthlyPayment = 9934 ether; // Monthly payment in wei
        originationFee = 10000 ether; // Origination fee in wei
        
        loanStartDate = 1736688000; // January 10, 2025
        disbursementDate = 1735776000; // February 1, 2025
        firstPaymentDueDate = 1737235200; // March 1, 2025
        loanTermEndDate = 1263033600; // January 10, 2030
        
        remainingBalance = loanAmount;
        loanDisbursed = false;
        loanDefaulted = false;
    }
    
    modifier onlyLender() {
        require(msg.sender == lender, "Only lender can call this function");
        _;
    }
    
    modifier onlyBorrower() {
        require(msg.sender == borrower, "Only borrower can call this function");
        _;
    }
    
    modifier loanIsActive() {
        require(!loanDefaulted, "Loan has been defaulted");
        require(loanDisbursed, "Loan has not been disbursed yet");
        _;
    }
    
    function disburseLoan() external onlyLender {
        require(!loanDisbursed, "Loan already disbursed");
        require(block.timestamp >= disbursementDate, "Cannot disburse loan yet");
        
        loanDisbursed = true;
        remainingBalance = loanAmount;
        
        emit LoanDisbursed(loanAmount, block.timestamp);
    }
    
    function makePayment() external payable onlyBorrower loanIsActive {
        require(msg.value == monthlyPayment, "Incorrect payment amount");
        require(block.timestamp >= firstPaymentDueDate, "Payment not due yet");
        
        remainingBalance -= msg.value;
        
        emit PaymentMade(msg.value, block.timestamp);
        
        if (remainingBalance <= 0) {
            loanDefaulted = true;
        }
    }
    
    function defaultLoan(string calldata reason) external onlyLender {
        require(!loanDefaulted, "Loan already in default");
        
        loanDefaulted = true;
        
        emit LoanDefaulted(reason);
    }
    
    function updateObligation(string calldata obligation) external onlyLender {
        emit ObligationsUpdated(obligation);
    }
    
    // Getters
    function getLoanDetails() external view returns (uint256, uint256, uint256, uint256, bool, bool) {
        return (loanAmount, monthlyPayment, originationFee, remainingBalance, loanDisbursed, loanDefaulted);
    }
}