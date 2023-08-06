@database.default
Feature: Categories
  As a user,
  I'd like to assign transactions to a category so that I can monitor spending
  in that category.

  Scenario: Add a category
    Given the following categories:
      | name | parent |
    When I run "bdgt category add cat1"
    Then the command output should equal:
      """
      Category 'cat1' created.
      """

  Scenario: Add a subcategory
    Given the following categories:
      | name   | parent |
      | parent |        |
    When I run "bdgt category add child --parent parent"
    Then the command output should equal:
      """
      Subcategory 'child' created.
      """

  Scenario: Delete a category
    Given the following categories:
      | name | parent |
      | cat1 |        |
    When I run "bdgt category delete cat1"
    Then the command output should equal:
      """
      Category 'cat1' deleted.
      """

  Scenario: Rename a category
    Given the following categories:
      | name | parent |
      | cat1 |        |
    When I run "bdgt category rename cat1 cat2"
    Then the command output should equal:
      """
      Category 'cat1' renamed to 'cat2'.
      """
