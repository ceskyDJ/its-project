import sys

import behave.runner
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait


@when('I select {input_name} "{item_name}"')
def step_impl(context: behave.runner.Context, input_name: str, item_name: str) -> None:
    browser: WebDriver = context.selenium

    if input_name == "Evaluation Scenario":
        # Has own tab
        menu_item = browser.find_element(By.ID, 'autotoc-item-autotoc-1')
        menu_item.click()

    if input_name == "Use Case provider":
        input_box_id = "formfield-form-widgets-use_case_provider"
        search_field_id = "s2id_autogen6"
    elif input_name == "Partner":
        input_box_id = "formfield-form-widgets-partners"
        search_field_id = "s2id_autogen4"
    elif input_name == "Evaluation Scenario":
        input_box_id = "formfield-form-widgets-evaluation_scenario"
        search_field_id = "s2id_autogen2"
    else:
        raise NotImplementedError

    # Move to root path (click on button with house icon)
    house_button = browser.find_element(By.XPATH, f"//div[@id='{input_box_id}']//a[@class='crumb']")
    house_button.click()

    # Enter name of the item to search
    search_field = browser.find_element(By.ID, search_field_id)
    search_field.send_keys(item_name)

    # Select searched item
    search_result = browser.find_element(
        By.XPATH, f"//div[@id='select2-drop']//li[1]//a[contains(@class, 'selectable')]"
    )
    WebDriverWait(browser, 15).until(EC.element_to_be_clickable(search_result)).click()


@then('I should see "{item_name}" in "{section_name}"')
def step_impl(context: behave.runner.Context, item_name: str, section_name: str) -> None:
    browser: WebDriver = context.selenium

    if section_name == "Use Case Provider":
        container_id = "form-widgets-use_case_provider"
    elif section_name == "Partners":
        container_id = "form-widgets-partners"
    elif section_name == "Evaluation Scenarios List":
        container_id = "form-widgets-evaluation_scenario"
    else:
        raise NotImplementedError

    displayed_items: list[WebElement] = browser.find_elements(
        By.XPATH,
        f"//span[@id='{container_id}']//span[contains(@class, 'contenttype-')]"
    )

    for item in displayed_items:
        if item.text.strip() == item_name:
            assert True
            return

    # Not found --> not displayed
    assert False


@then('I should find Use Case "{use_case_name}" on "Use Cases" page')
def step_impl(context: behave.runner.Context, use_case_name: str) -> None:
    browser: WebDriver = context.selenium

    # Bad Use Case's name (or forgotten creation in current scenario - use: Given I have Use Case "{use_case_name}"
    if use_case_name not in context.urls:
        raise ValueError(f"Use Case {use_case_name} isn't known in current scenario")

    context.execute_steps(f'Given I went to page "Use Cases"')

    displayed_use_cases = browser.find_elements(
        By.XPATH,
        "//div[@id='faceted-results']//tr//a[contains(@class, 'contenttype-use_case')]"
    )

    for use_case in displayed_use_cases:
        use_case_detail_url = context.urls[use_case_name]

        if use_case.get_attribute("href") == use_case_detail_url.replace("/view", ""):
            assert True
            return

    assert False


@then('I should not find Use Case "{use_case_name}" on "Use Cases" page')
def step_impl(context: behave.runner.Context, use_case_name: str) -> None:
    context.execute_steps('Given I went to page "Use Cases"')

    # It is only reversed
    try:
        context.execute_steps(f'Then I should find Use Case "{use_case_name}" on "Use Cases" page')

        assert False
    except AssertionError:
        assert True
