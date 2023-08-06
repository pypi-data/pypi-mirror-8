@database.default
Feature: Reconcile
  As a user
  I want to reconcile transaction

  Scenario: Reconcile transactions
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
    When I run "bdgt tx reconcile 1,2"
    Then the command output should equal:
      """
      Reconciled 2 transactions
      """
    And account "test" has 0 unreconciled transactions
    And the command exit code should be 0
