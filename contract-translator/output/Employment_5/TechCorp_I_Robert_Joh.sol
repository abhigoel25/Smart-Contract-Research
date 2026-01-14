// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    address public employer;
    address public employee;

    uint256 public salary;
    uint256 public performanceBonus;
    uint256 public stockOptions;

    uint256 public commencementDate;
    uint256 public endDate;

    string[] public employeeObligations;
    string[] public employerObligations;
    string[] public specialTerms;
    string[] public terminationConditions;

    enum AgreementStatus { Active, Terminated }
    AgreementStatus public status;

    event EmploymentStarted(address employee, uint256 commencementDate);
    event EmploymentTerminated(address employee, uint256 terminationDate, string reason);
  
    modifier onlyEmployer() {
        require(msg.sender == employer, "Only employer can call this function");
        _;
    }

    modifier onlyEmployee() {
        require(msg.sender == employee, "Only employee can call this function");
        _;
    }

    constructor(
        address _employee,
        uint256 _salary,
        uint256 _performanceBonus,
        uint256 _stockOptions,
        uint256 _commencementDate,
        uint256 _endDate
    ) {
        employer = msg.sender; // Contract deployer is the employer
        employee = _employee;
        salary = _salary;
        performanceBonus = _performanceBonus;
        stockOptions = _stockOptions;

        commencementDate = _commencementDate;
        endDate = _endDate;

        status = AgreementStatus.Active;

        // Obligations
        employeeObligations.push("Serve as Senior Software Engineer, developing enterprise-level applications, mentoring junior developers, and making architectural decisions.");
        employerObligations.push("Provide salary and benefits as outlined in the agreement.");

        // Special terms
        specialTerms.push("Confidentiality of all proprietary information must be maintained.");
        specialTerms.push("Non-Compete Period: 12 months post-employment within 100-mile radius of headquarters.");

        // Termination conditions
        terminationConditions.push("Either party may terminate with 30 days written notice.");
        terminationConditions.push("3 months base salary upon termination without cause.");
        terminationConditions.push("Termination for cause includes breach of confidentiality, gross negligence, or policy violation.");

        emit EmploymentStarted(_employee, _commencementDate);
    }

    function terminateEmployment(string memory reason) external {
        require(status == AgreementStatus.Active, "Employment agreement is already terminated.");
        require(msg.sender == employer || msg.sender == employee, "Only employer or employee can terminate.");

        status = AgreementStatus.Terminated;

        emit EmploymentTerminated(employee, block.timestamp, reason);
    }

    function getFinancialTerms()
        external
        view
        returns (uint256, uint256, uint256)
    {
        return (salary, performanceBonus, stockOptions);
    }

    function getEmployeeObligations() external view returns (string[] memory) {
        return employeeObligations;
    }

    function getEmployerObligations() external view returns (string[] memory) {
        return employerObligations;
    }

    function getSpecialTerms() external view returns (string[] memory) {
        return specialTerms;
    }

    function getTerminationConditions() external view returns (string[] memory) {
        return terminationConditions;
    }

    function currentStatus() external view returns (AgreementStatus) {
        return status;
    }
}