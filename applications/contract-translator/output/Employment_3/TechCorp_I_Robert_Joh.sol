// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    address public employer;
    address public employee;

    struct FinancialTerms {
        uint256 amount;
        string currency;
        string purpose;
        string frequency;
        string dueDate;
    }

    struct Obligation {
        string party;
        string description;
    }

    struct SpecialTerm {
        string term;
    }

    FinancialTerms[] public financialTerms;
    Obligation[] public obligations;
    SpecialTerm[] public specialTerms;

    enum EmploymentStatus { Active, Terminated }
    EmploymentStatus public status;

    event CompensationPaid(address indexed recipient, uint256 amount);
    event Terminated(address indexed party);
    
    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can perform this action");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can perform this action");
        _;
    }

    constructor(address _employee) {
        employer = msg.sender; // The address deploying the contract is the employer
        employee = _employee;
        status = EmploymentStatus.Active;
        
        // Setup financial terms
        financialTerms.push(FinancialTerms(150000 * 10 ** 18, "USD", "salary", "annual", "monthly"));
        financialTerms.push(FinancialTerms(25000 * 10 ** 18, "USD", "performance bonus", "annual", ""));
        
        // Setup obligations
        obligations.push(Obligation("employee", "Serve as Senior Software Engineer, developing enterprise-level applications, mentoring junior developers, and making architectural decisions"));
        obligations.push(Obligation("employer", "Provide compensation, benefits, and support as outlined in the agreement"));
        
        // Setup special terms
        specialTerms.push(SpecialTerm("At-will employment; either party may terminate with 30 days written notice"));
        specialTerms.push(SpecialTerm("3 months base salary severance upon termination without cause"));
        specialTerms.push(SpecialTerm("12 months non-compete period within 100-mile radius of headquarters"));
    }

    function payCompensation() external onlyEmployer {
        require(status == EmploymentStatus.Active, "Employment is not active");

        // Transfer salary to employee
        // Note: In practice, we would handle actual ETH transfers,
        // Here we would typically interact with an off-chain payment processor for USD payments
        emit CompensationPaid(employee, financialTerms[0].amount);
    }

    function terminateEmployment() external {
        require(status == EmploymentStatus.Active, "Employment is already terminated");
        status = EmploymentStatus.Terminated;
        
        // Log the termination event
        emit Terminated(msg.sender);
    }

    function getFinancialTerms() external view returns (FinancialTerms[] memory) {
        return financialTerms;
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function getSpecialTerms() external view returns (SpecialTerm[] memory) {
        return specialTerms;
    }
}