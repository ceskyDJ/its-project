import behave.runner
from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from helpers import javascript_click


@given('State of {} "{item_name}" is "{state}"')
def step_impl(context: behave.runner.Context, _, item_name: str, state: str) -> None:
    browser: WebDriver = context.selenium

    # Bad item's name (or forgotten creation in current scenario - use: Given I have {tool_type} "{tool_name}"
    if item_name not in context.urls:
        raise ValueError(f"Tool {item_name} isn't known in current scenario")

    # Go to item's detail page
    browser.get(context.urls[item_name])

    # Open state menu
    menu_button = browser.find_element(By.XPATH, "//li[@id='plone-contentmenu-workflow']/a")
    javascript_click(browser, menu_button)

    # Get current state for check if it equals to wanted state or doesn't
    current_state_element = browser.find_element(
        By.XPATH,
        "//li[@id='plone-contentmenu-workflow']//li[@class='plone-toolbar-submenu-header']"
        "//span[contains(@class, 'state-')]"
    )
    current_state = current_state_element.text.strip()

    if current_state == state:
        # Current state is the final one
        return

    if state == "Private":
        if current_state == "Published":
            # Hide published item
            button_id = "workflow-transition-retract"
        else:
            # Reject on review
            button_id = "workflow-transition-reject"
    elif state == "Pending review":
        button_id = "workflow-transition-submit"
    elif state == "Published":
        button_id = "workflow-transition-publish"
    else:
        raise NotImplementedError

    change_state_button = browser.find_element(By.ID, button_id)
    change_state_button.click()


@when('I submit for publication {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    context.execute_steps(f'Given State of {item_type} "{item_name}" is "Pending review"')


@when('I reject submitting of the {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    context.execute_steps(f'Given State of {item_type} "{item_name}" is "Private"')


@when('I approve the {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    context.execute_steps(f'Given State of {item_type} "{item_name}" is "Published"')


@when('I publish {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    context.execute_steps(f'Given State of {item_type} "{item_name}" is "Published"')


@then('State of {item_type} "{item_name}" should be "{state}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str, state: str) -> None:
    browser: WebDriver = context.selenium

    # Bad item's name (or forgotten creation in current scenario - use: Given I have {item_type} "{item_name}"
    if item_name not in context.urls:
        raise ValueError(f"{item_type} {item_name} isn't known in current scenario")

    # Go to item's detail page
    browser.get(context.urls[item_name])

    # Open state menu
    menu_button = browser.find_element(By.XPATH, "//li[@id='plone-contentmenu-workflow']/a")
    javascript_click(browser, menu_button)

    # Get current state for check if it equals to wanted state or doesn't
    current_state_element = browser.find_element(
        By.XPATH,
        "//li[@id='plone-contentmenu-workflow']//li[@class='plone-toolbar-submenu-header']"
        "//span[contains(@class, 'state-')]"
    )

    assert current_state_element.text.strip() == state
