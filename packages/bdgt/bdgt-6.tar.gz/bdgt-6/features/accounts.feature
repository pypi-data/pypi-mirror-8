@database.default
Feature: Accounts
  As a user
  I want to manage multiple accounts
  So that transactions can be added to them.

  Scenario: Add an account
    When I run "bdgt account add test 987654321"
    Then the command output should equal:
      """
      Account 'test' created
      """
    And account "test" exists
    And the command exit code should be 0

  Scenario: Delete an account
    Given the following accounts
      | name     | number |
      | cash     | 12345  |
      | personal | 34567  |
      | savings  | 54623  |
    When I run "bdgt account delete cash"
    Then the command output should equal:
      """
      Account 'cash' deleted
      """
    And account "cash" doesn't exist
    And the command exit code should be 0

  Scenario: List accounts
    Given the following accounts
      | name     | number |
      | cash     | 12345  |
      | personal | 34567  |
      | savings  | 54623  |
    When I run "bdgt account list"
    Then the command output should equal:
      """
      cash
      personal
      savings
      """
    And the command exit code should be 0
