// SOLIDITY COMPILATION ERROR
// Error: An error occurred during execution
> command: `C:\Users\abhin\.solcx\solc-v0.8.0\solc.exe --combined-json abi,bin --optimize --optimize-runs 200 -`
> return code: `1`
> stdout:

> stderr:
Expected primary expression.
  --> <stdin>:45:1:
   |
45 | 
   | ^
// This contract failed to compile

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LoanAgreement {
    event LoanInitialized(address lender, address borrower, uint256 loanAmount);
    event PaymentMade(address borrower, uint256 amount);
    event DefaultOccurred(address borrower);

    address public lender;
    address public borrower;
    uint256 public loanAmount;
    uint256 public monthlyPayment;
    uint256 public originationFee;
    uint256 public latePaymentFeePercent;
    bool public isActive;

    constructor(address _lender, address _borrower) {
        lender = _lender;
        borrower = _borrower;
        loanAmount = 500000 * 1 ether; // Representing USD as wei
        monthlyPayment = 9934 * 1 ether;
        originationFee = 10000 * 1 ether;
        latePaymentFeePercent = 5; // 5%
        isActive = true;
        emit LoanInitialized(lender, borrower, loanAmount);
    }

    function makePayment(uint256 amount) external returns (bool) {
        require(msg.sender == borrower, "Only borrower can make payments");
        require(amount >= monthlyPayment, "Insufficient payment amount");

        emit PaymentMade(borrower, amount);
        return true;
    }

    function triggerDefault() external returns (bool) {
        require(msg.sender == lender, "Only lender can trigger default");
        isActive = false;
        emit DefaultOccurred(borrower);
        return true;
    }

    function getLoanDetails() external view returns (address, address, uint256, uint256) {
        return (lender, borrower, loanAmount, monthlyPayment);