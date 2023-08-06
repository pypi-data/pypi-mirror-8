@database.default
Feature: Budget
  As a user,
  I'd like to budget my spending by setting spending limits on categories
  So that I can track my spending in each category.

  Scenario: Set a weekly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 week 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per week
      """
    And "cat1" has 1 budget items
    And the command exit code should be 0

  Scenario: Set a monthly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 month 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per month
      """
    And "cat1" has 1 budget items
    And the command exit code should be 0

  Scenario: Set a quaterly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 quarter 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per quarter
      """
    And "cat1" has 1 budget items
    And the command exit code should be 0

  Scenario: Set a yearly spending limit
    Given the following categories
      | name |
      | cat1 |
    When I run "bdgt set cat1 year 150.00"
    Then the command output should equal:
      """
      Budget for "cat1" is set to 150.00 per year
      """
    And "cat1" has 1 budget items
    And the command exit code should be 0

  Scenario: View budget progress
    Given the following accounts
      | name | number    |
      | test | 987654321 |
    And the following categories
      | name |
      | cat1 |
      | cat2 |
      | cat3 |
    And the following budget items
      | category | period | amount |
      | cat1     | month  | 100.00 |
      | cat2     | month  | 135.00 |
      | cat3     | month  | 135.00 |
    And the following transactions
      | account | date_time  | desc | amount  | reconciled | category |
      | test    | 01-01-2014 | desc |  -30.00 | False      | cat1     |
      | test    | 02-01-2014 | desc |  -30.00 | False      | cat1     |
      | test    | 03-01-2014 | desc |  -30.00 | False      | cat1     |
      | test    | 04-01-2014 | desc | -100.50 | False      | cat2     |
      | test    | 05-01-2014 | desc |  -10.00 | False      | cat2     |
      | test    | 06-01-2014 | desc |  -75.00 | False      | cat2     |
      | test    | 07-01-2014 | desc | -115.00 | False      | cat2     |
      | test    | 07-01-2014 | desc |  150.13 | False      | cat3     |
      | test    | 08-01-2014 | desc |  -12.25 | False      | cat3     |
      | test    | 09-01-2014 | desc |  -34.10 | False      | cat3     |
    When I run "bdgt status 01 2014"
    Then the command output should equal:
      """
      | category | budget |         spent |       remaining | transactions |
      |     cat1 | 100.00 |   90.00 (90%) |     10.00 (10%) |            3 |
      |     cat2 | 135.00 | 300.50 (223%) | -165.50 (-123%) |            4 |
      |     cat3 | 135.00 |   46.35 (34%) |     88.65 (66%) |            2 |
      """
    And the command exit code should be 0
