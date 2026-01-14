// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmploymentAgreement {
    event AgreementCreated(address employer, address employee);
    event ObligationsUpdated(string party, string description);

    address public employer;
    address public employee;

    string public employerName;
    string public employeeName;

    uint public salaryAmount;
    uint public monthlyPaymentAmount;
    uint public bonusAmount;
    uint public stockOptionsAmount;

    string public employeeObligation;
    string public employerObligation;

    constructor(
        address _employer,
        address _employee,
        string memory _employerName,
        string memory _employeeName
    ) {
        employer = _employer;
        employee = _employee;
        employerName = _employerName;
        employeeName = _employeeName;

        salaryAmount = 150000;
        monthlyPaymentAmount = 12500;
        bonusAmount = 25000;
        stockOptionsAmount = 5000;

        employeeObligation = "Serve as Senior Software Engineer and fulfill responsibilities including developing enterprise-level applications, mentoring junior developers, and making architectural decisions.";
        employerObligation = "Provide compensation and benefits as stated in the agreement.";

        emit AgreementCreated(employer, employee);
    }

    function getEmployer() public view returns (address) {
        return employer;
    }

    function getEmployee() public view returns (address) {
        return employee;
    }

    function getSalaryAmount() public view returns (uint) {
        return salaryAmount;
    }

    function getMonthlyPaymentAmount() public view returns (uint) {
        return monthlyPaymentAmount;
    }

    function getBonusAmount() public view returns (uint) {
        return bonusAmount;
    }

    function getStockOptionsAmount() public view returns (uint) {
        return stockOptionsAmount;
    }

    function getEmployeeObligation() public view returns (string memory) {
        return employeeObligation;
    }

    function getEmployerObligation() public view returns (string memory) {
        return employerObligation;
    }
}