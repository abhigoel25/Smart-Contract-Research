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
        string dueDate;
    }

    struct Obligation {
        string party;
        string description;
    }

    FinancialTerm[] public financialTerms;
    Obligation[] public obligations;

    enum TerminationReason { None, WithoutCause, ForCause }
    mapping(address => uint256) public salaries;
    mapping(address => bool) public isTerminated;
    uint256 public terminationNoticePeriod = 30 days;
    uint256 public terminationBenefits = 3 ether; // Assuming 1 ether = 1 base salary for simplicity
    TerminationReason public terminationReason;

    event EmploymentStarted(address indexed employee, address indexed employer, uint256 startDate);
    event EmploymentTerminated(address indexed employee, address indexed employer, TerminationReason reason);
    event PaymentMade(address indexed payee, uint256 amount, string currency, string purpose);

    constructor(address _employee) {
        employer = msg.sender; // The contract deployer is the employer
        employee = _employee;

        // Initialize financial terms
        financialTerms.push(FinancialTerm(150000 ether, "USD", "salary", "annual", "monthly"));
        financialTerms.push(FinancialTerm(25000 ether, "USD", "performance bonus", "annual", ""));
        financialTerms.push(FinancialTerm(1, "unit", "stock options", "vest over 4 years with 1-year cliff", ""));

        // Initialize obligations
        obligations.push(Obligation("Employee", "Serve as Senior Software Engineer and report to Chief Technology Officer, develop enterprise-level applications, mentor junior developers, and make architectural decisions."));
        obligations.push(Obligation("Employer", "Provide employee with salary, performance bonuses, health insurance, retirement benefits, and paid time off."));

        emit EmploymentStarted(employee, employer, block.timestamp);
    }

    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can call this function.");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can call this function.");
        _;
    }

    function paySalary() external onlyEmployer {
        require(!isTerminated[employee], "Employee is terminated.");
        // Logic to pay salary (implement the actual payment logic as per the payment integration)
        emit PaymentMade(employee, financialTerms[0].amount, financialTerms[0].currency, financialTerms[0].purpose);
    }

    function payBonus() external onlyEmployer {
        require(!isTerminated[employee], "Employee is terminated.");
        // Logic to pay bonus (implement the actual payment logic as per the payment integration)
        emit PaymentMade(employee, financialTerms[1].amount, financialTerms[1].currency, financialTerms[1].purpose);
    }

    function terminateEmployment(TerminationReason _reason) external {
        require(!isTerminated[employee], "Employee is already terminated.");
        require(msg.sender == employer || (msg.sender == employee && _reason == TerminationReason.WithoutCause), "Unauthorized termination.");

        isTerminated[employee] = true;
        terminationReason = _reason;

        // Implement termination benefits logic here as needed.

        emit EmploymentTerminated(employee, employer, _reason);
    }

    function getObligations() external view returns (Obligation[] memory) {
        return obligations;
    }

    function getFinancialTerms() external view returns (FinancialTerm[] memory) {
        return financialTerms;
    }

    function isEmployeeTerminated() external view returns (bool) {
        return isTerminated[employee];
    }
}