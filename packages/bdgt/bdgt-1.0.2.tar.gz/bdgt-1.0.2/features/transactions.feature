Feature: Transactions
  As a user
  I want to manage transactions

  Scenario: List transactions
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name |
      | cat1 |
      | cat2 |
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
