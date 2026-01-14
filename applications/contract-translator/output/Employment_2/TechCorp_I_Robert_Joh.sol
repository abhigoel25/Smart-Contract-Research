// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    address public employer;
    address public employee;

    struct FinancialTerm {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
    }

    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;
    
    string[] public specialTerms;
    string[] public terminationConditions;

    event FinancialTermAdded(uint256 amount, string currency, string purpose);
    event ObligationAdded(string party, string description);
    event EmploymentTerminated(address terminatedBy);
    event SalaryPaid(address employee, uint256 amount, string currency);

    constructor() {
        employer = msg.sender; // Employer is the contract creator
        employee = address(0); // Employee will be set later
    }

    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can perform this action.");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can perform this action.");
        _;
    }

    function setEmployee(address _employee) external onlyEmployer {
        require(_employee != address(0), "Invalid employee address.");
        employee = _employee;
    }

    function addFinancialTerm(uint256 _amount, string calldata _currency, string calldata _purpose, string calldata _frequency) external onlyEmployer {
        financialTerms.push(FinancialTerm(_amount, _currency, _purpose, _frequency));
        emit FinancialTermAdded(_amount, _currency, _purpose);
    }

    function addObligation(string calldata _party, string calldata _description) external onlyEmployer {
        obligations.push(Obligation(_party, _description));
        emit ObligationAdded(_party, _description);
    }

    function addSpecialTerm(string calldata _term) external onlyEmployer {
        specialTerms.push(_term);
    }

    function addTerminationCondition(string calldata _condition) external onlyEmployer {
        terminationConditions.push(_condition);
    }

    function paySalary() external onlyEmployer {
        require(financialTerms.length > 0, "No financial terms available.");
        require(employee != address(0), "Employee is not set.");
        
        // Salary calculation
        uint256 salaryAmount;
        for (uint256 i = 0; i < financialTerms.length; i++) {
            if (keccak256(abi.encodePacked(financialTerms[i].purpose)) == keccak256(abi.encodePacked("salary"))) {
                salaryAmount = financialTerms[i].amount;
                break;
            }
        }
        // Assume the transfer is happening here based on the 'amount' and 'currency'.
        // In practice, you would need to use an ERC20 token contract for USD equivalent or a payment service.
        
        emit SalaryPaid(employee, salaryAmount, "USD");
    }

    function terminateEmployment() external onlyEmployer {
        // Logic for termination and potential severance can go here.
        emit EmploymentTerminated(msg.sender);
    }

    // Other functions for managing obligations, conditions, and approvals can be added.
}