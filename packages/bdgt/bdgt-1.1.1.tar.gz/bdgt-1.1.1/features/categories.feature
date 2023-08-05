Feature: Categories
  As a user,
  I'd like to assign transactions to a category so that I can monitor spending
  in that category.

  Scenario: Add transaction to a category
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
      Assigned 1 transactions to the cat1 category
      """
    And category "cat1" exists
    And category "cat1" has 1 transactions
    And the command exit code should be 0

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
    When I run "bdgt tx assign cat1 1-3,4"
    Then the command output should equal:
      """
      Assigned 4 transactions to the cat1 category
      """
    And category "cat1" exists
    And category "cat1" has 4 transactions
    And the command exit code should be 0

  Scenario: Remove transaction from a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name |
      | cat1 |
      | cat2 |
    And the following transactions
      | account | date_time  | desc  | amount  | reconciled | category |
      | test    | 01-01-2014 | desc1 | 100.00  | False      | cat1     |
      | test    | 10-05-2007 | desc2 | -76.00  | False      | cat2     |
    When I run "bdgt tx unassign 1"
    Then the command output should equal:
      """
      Unassigned 1 transactions from their category
      """
    And category "cat1" exists
    And category "cat1" has 0 transactions
    And the command exit code should be 0

  Scenario: Remove multiple transactions from a category
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name |
      | cat1 |
      | cat2 |
      | cat3 |
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
    And category "cat1" exists
    And category "cat1" has 0 transactions
    And the command exit code should be 0
