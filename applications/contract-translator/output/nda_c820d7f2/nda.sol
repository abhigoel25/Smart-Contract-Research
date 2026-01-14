// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MutualNonDisclosureAgreement {

    struct Party {
        string name;
        string role;
        string addressLine;
        string email;
        string entityType;
    }

    struct Date {
        string dateType;
        string value; // For ease of use, storing date as string
        uint dayOfMonth;
        string frequency;
    }

    struct Obligation {
        string party;
        string description;
        string deadline;
        string penaltyForBreach;
    }

    struct Conditions {
        string exceptions;
    }

    struct TerminationConditions {
        string[] conditions;
    }

    Party[2] public parties;
    Date public startDate;
    Obligation[] public obligations;
    string[] public specialTerms;
    Conditions public conditions;
    TerminationConditions public terminationConditions;

    event NDAIneffective(string reason);
    event ObligationFulfilled(string obligationDescription);

    constructor() {
        parties[0] = Party("InnovateTech Ventures, LLC", "Disclosing Party", "333 Startup Way, San Francisco, CA 94105", "", "company");
        parties[1] = Party("FutureInvest Capital Partners", "Receiving Party", "777 Investment Drive, New York, NY 10005", "", "company");

        startDate = Date("start", "January 8, 2025", 8, "");

        obligations.push(Obligation("Receiving Party", "Maintain strict confidentiality and protect information with reasonable security measures.", "", ""));
        obligations.push(Obligation("Receiving Party", "Limit disclosure to employees/contractors with need-to-know basis.", "", ""));
        obligations.push(Obligation("Receiving Party", "Use information only for stated evaluation purposes.", "", ""));
        obligations.push(Obligation("Receiving Party", "Not reverse-engineer or attempt to derive underlying principles.", "", ""));

        specialTerms.push("Confidentiality Period: 3 years from disclosure date.");
        specialTerms.push("Obligations survive termination of discussions.");
        specialTerms.push("Trade Secrets: Protected for as long as they remain trade secrets under applicable law.");

        conditions = Conditions("Receiving Party may disclose if required by law/court order with prior written notice to Disclosing Party.");
        terminationConditions = TerminationConditions(new string[](1));
        terminationConditions.conditions[0] = "Obligations survive termination of discussions.";
    }

    // Getters for Parties
    function getDisclosingParty() public view returns (Party memory) {
        return parties[0];
    }

    function getReceivingParty() public view returns (Party memory) {
        return parties[1];
    }

    // Get Start Date
    function getStartDate() public view returns (Date memory) {
        return startDate;
    }

    // Get Obligations
    function getObligations() public view returns (Obligation[] memory) {
        return obligations;
    }

    // Get Special Terms
    function getSpecialTerms() public view returns (string[] memory) {
        return specialTerms;
    }

    // Get Conditions
    function getConditions() public view returns (Conditions memory) {
        return conditions;
    }

    // Get Termination Conditions
    function getTerminationConditions() public view returns (TerminationConditions memory) {
        return terminationConditions;
    }

    // Function to fulfill an obligation
    function fulfillObligation(uint obligationIndex) public returns (bool) {
        if (obligationIndex < obligations.length) {
            emit ObligationFulfilled(obligations[obligationIndex].description);
            return true;
        } else {
            emit NDAIneffective("Invalid obligation index.");
            return false;
        }
    }
}