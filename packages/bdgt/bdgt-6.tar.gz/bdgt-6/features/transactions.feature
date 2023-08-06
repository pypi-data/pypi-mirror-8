@database.default
Feature: Transactions
  As a user
  I want to manage transactions

  Scenario: List transactions
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name | parent |
      | cat1 |        |
      | cat2 |        |
    And the following transactions
      | account | date_time  | desc  | amount | reconciled | category |
      | test    | 01-01-2014 | desc1 | 100.00 | False      | cat1     |
      | test    | 10-05-2007 | desc2 | -76.00 | False      | cat2     |
    When I run "bdgt tx list test"
    Then the command output should equal:
      """
      | 2 | 2007-05-10 | desc2 | cat2 | N | [31m-76.00[39m |
      | 1 | 2014-01-01 | desc1 | cat1 | N | [32m100.00[39m |
      """
    And the command exit code should be 0

  Scenario: Add a transaction to a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following transactions
      | account | date_time  | desc  | amount  | reconciled |
      | test    | 01-01-2014 | desc1 | 100.00  | False      |
      | test    | 10-05-2007 | desc2 | -76.00  | False      |
    And the following categories
      | name | parent |
      | cat1 |        |
    When I run "bdgt tx assign cat1 1"
    Then the command output should equal:
      """
      Assigned 1 transactions to the cat1 category
      """
    And category "cat1" has 1 transactions
    And the command exit code should be 0

  Scenario: Report an error when adding a transaction to a category that
            doesn't exist.
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following transactions
      | account | date_time  | desc  | amount  | reconciled |
      | test    | 01-01-2014 | desc1 | 100.00  | False      |
      | test    | 10-05-2007 | desc2 | -76.00  | False      |
    When I run "bdgt tx assign cat1 1"
    Then the command output should equal:
      """
      Error: Category 'cat1' not found.
      """
    And the command exit code should be 1

  Scenario: Add multiple transactions to a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following transactions
      | account | date_time  | desc  | amount | reconciled |
      | test    | 01-01-2014 | desc1 | 100.00 | False      |
      | test    | 10-05-2007 | desc2 | -76.00 | False      |
      | test    | 23-04-2008 | desc3 |   6.57 | False      |
      | test    | 17-09-2014 | desc4 |  12.30 | False      |
    And the following categories
      | name | parent |
      | cat1 |        |
    When I run "bdgt tx assign cat1 1-3,4"
    Then the command output should equal:
      """
      Assigned 4 transactions to the cat1 category
      """
    And category "cat1" has 4 transactions
    And the command exit code should be 0

  Scenario: Remove transaction from a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name | parent |
      | cat1 |        |
      | cat2 |        |
    And the following transactions
      | account | date_time  | desc  | amount  | reconciled | category |
      | test    | 01-01-2014 | desc1 | 100.00  | False      | cat1     |
      | test    | 10-05-2007 | desc2 | -76.00  | False      | cat2     |
    When I run "bdgt tx unassign 1"
    Then the command output should equal:
      """
      Unassigned 1 transactions from their category
      """
    And category "cat1" has 0 transactions
    And the command exit code should be 0

  Scenario: Remove multiple transactions from a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name | parent |
      | cat1 |        |
      | cat2 |        |
      | cat3 |        |
    And the following transactions
      | account | date_time  | desc  | amount | reconciled | category |
      | test    | 01-01-2014 | desc1 | 100.00 | False      | cat1     |
      | test    | 10-05-2007 | desc2 | -76.00 | False      | cat1     |
      | test    | 23-04-2008 | desc3 |   6.57 | False      | cat2     |
      | test    | 17-09-2014 | desc4 |  12.30 | False      | cat3     |
    When I run "bdgt tx unassign 1-3,4"
    Then the command output should equal:
      """
      Unassigned 4 transactions from their category
      """
    And category "cat1" has 0 transactions
    And the command exit code should be 0
