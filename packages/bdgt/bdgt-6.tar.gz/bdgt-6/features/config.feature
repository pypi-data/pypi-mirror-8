@database.none
Feature: Config
  As a user I want to provider common command line arguments using a config
  file.

  Scenario: View effective configuration without config file
    When I run "bdgt config"
    Then the command output should contain:
      """
      .bdgt/bdgt.db
      """
    And the command exit code should be 0

  Scenario: View effective configuration with config file
    Given a file named "test.cfg" with:
      """
      [bdgt]
      database = sqlite:///example.db
      """
    When I run "bdgt -c test.cfg config"
    Then the command output should equal:
      """
      database = sqlite:///example.db
      """
    And the command exit code should be 0

  Scenario: View effective configuration with empty config file
    Given a file named "test.cfg" with:
      """
      """
    When I run "bdgt -c test.cfg config"
    Then the command output should contain:
      """
      .bdgt/bdgt.db
      """
    And the command exit code should be 0

  @wip
  Scenario: Use the configuration file ~/.bdgtrc by default if it exists
    Given a file named "~/.bdgtrc" with:
      """
      [bdgt]
      database = sqlite:///example.db
      """
    When I run "bdgt config"
    Then the command output should equal:
      """
      database = sqlite:///example.db
      """
    And the command exit code should be 0
