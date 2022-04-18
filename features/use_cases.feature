Feature: Manipulation with Use Cases

  Background:
    Given I am logged in as user with privileges to manage Use Cases

  Scenario: [1] Opening form for adding new Use Case
    Given I went to page "Use Cases"
    When I open form for creating Use Cases
    Then I should be in "Add Use Case" form
    And "Default" tab should be opened

  Scenario: [2] Creating Use Case with only required fields (without relations)
    Given I opened form "Add Use Case"
    When I fill in required fields
    And I save Add Use Case form
    Then I should be on page with created Use Case's detail
    And I should see information message "Item created"

  Scenario: [3] Creating Use Case with selected owner Organization and partner Organization and Evaluation Scenario
    Given I opened form "Add Use Case"
    And I have Organization "BUT"
    And I have Organization "Nothing"
    And I have Evaluation Scenario "Complex testing eval scenario"
    When I fill in required fields
    And I select Use Case provider "BUT"
    And I select partner "Nothing"
    And I select evaluation scenario "Complex testing eval scenario"
    And I save Add Use Case form
    Then I should be on page with created Use Case's detail
    And I should see information message "Item created"
    And I should see "BUT" in "Use Case Provider"
    And I should see "Nothing" in "Partners"
    And I should see "Complex testing eval scenario" in "Evaluation Scenarios List"

  Scenario: [4] Publishing Use Case for consumers
    Given I have Use Case "Testing UC"
    When I change Use Case "Testing UC" state to "Published"
    And I log out
    Then I should find Use Case "Testing UC" on "Use Cases" page

  Scenario: [5] Hide Use Case for consumers
    Given I have Use Case "Another UC"
    When I change Use Case "Testing UC" state to "Private"
    And I log out
    Then I should not find Use Case "Another UC" on "Use Cases" page

  Scenario: [6] Deleting a Use Case
    Given I have Use Case "UC for deletion"
    When I delete the Use Case "UC for deletion"
    Then I should not find Use Case "UC for deletion" on "Use Cases" page

  Scenario: [7] Add new Evaluation Scenario to Use Case
    Given I have Use Case "Edit UC"
    And I have Evaluation Scenario "Brand new Evaluation Scenario"
    And I am in the edit form of Use Case "Edit UC"
    When I add Evaluation Scenario "Brand new Evaluation Scenario" to Use Case "Edit UC"
    And I save edit form
    Then I should be on detail page of Use Case "Edit UC"
    And I should see information message "Changes saved"
    And I should see Scenario List "Brand new Evaluation Scenario" in the list of scenarios
