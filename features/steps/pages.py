import behave.runner
from behave import *
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from helpers import javascript_click


@given('I opened form "{form_name}"')
def step_impl(context: behave.runner.Context, form_name: str) -> None:
    browser: WebDriver = context.selenium

    if form_name.startswith("Add"):
        menu_button = browser.find_element(By.XPATH, "//li[@id='plone-contentmenu-factories']/a")
        try:
            javascript_click(browser, menu_button)
        except ElementClickInterceptedException:
            # Standard Selenium click not working, so try to click with JavaScript
            browser.execute_script("arguments[0].click();", menu_button)

        form_name_lowercase = form_name.lower()
        form_name_snake_case = form_name_lowercase.replace(" ", "_")
        form_button_id = form_name_snake_case[4:]  # Skip "add_"

        # Standard uses plural form
        if form_name == "Add Standard":
            form_button_id += "s"

        open_form_button = browser.find_element(By.ID, form_button_id)
        try:
            open_form_button.click()
        except ElementClickInterceptedException:
            # Standard Selenium click not working, so try to click with JavaScript
            browser.execute_script("arguments[0].click();", open_form_button)
    else:
        raise NotImplementedError


@given('I am in the edit form of {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    context.execute_steps(f'When I open "Edit {item_type}" form for {item_type} "{item_name}"')


@when('I open "Edit {}" form for {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, _, item_type: str, item_name: str) -> None:
    browser: WebDriver = context.selenium

    # Bad item's name (or forgotten creation in current scenario - use: Given I have {item_type} "{item_name}"
    if item_name not in context.urls:
        raise ValueError(f"{item_type} {item_name} isn't known in current scenario")

    # Save information about edited item's name
    context.item_name = item_name

    # Load item's view
    browser.get(context.urls[item_name])

    menu_button = browser.find_element(By.ID, "contentview-edit")
    javascript_click(browser, menu_button)


@then('I should be on page with {detail_type}\'s detail')
def step_impl(context: behave.runner.Context, detail_type: str) -> None:
    browser: WebDriver = context.selenium

    # {detail type} looks like: "edited Method", "edited Tool", etc.
    page_name_parts = detail_type.split(" ")
    # The first word is action name (see below)
    action_name = page_name_parts[0]

    # Detail shows up after form submission, only some forms are supported
    # Here a form is represented by action, which it does with items
    if action_name not in ["created", "edited"]:
        raise NotImplementedError

    main_heading = browser.find_element(By.XPATH, "//h1[@class='documentFirstHeading']")
    assert main_heading.text == context.item_name


@then('I should see page {message_type} message "{message_content}"')
def step_impl(context: behave.runner.Context, message_type: str, message_content: str) -> None:
    browser: WebDriver = context.selenium

    if message_type == "information":
        type_name = "Info"
    elif message_type == "error":
        type_name = "Error"
    else:
        raise NotImplementedError(f"Status message check of type {message_type} isn't supported")

    message_element = browser.find_element(
        By.XPATH,
        "//aside[@id='global_statusmessage']//div[contains(@class, 'portalMessage')]"
    )

    assert message_element.text.strip() == f"{type_name} {message_content}"


@then('I should be redirected to page "{page_name}"')
def step_impl(context: behave.runner.Context, page_name: str) -> None:
    browser: WebDriver = context.selenium

    if page_name == "Insufficient Privileges":
        correct_url = f"{context.url}/insufficient-privileges"
    else:
        raise NotImplementedError

    assert browser.current_url == correct_url


@given('I went to page "{page_name}"')
def step_impl(context: behave.runner.Context, page_name: str) -> None:
    browser: WebDriver = context.selenium

    if page_name == "Use Cases":
        menu_button_class = "use-cases"
    else:
        raise NotImplementedError

    menu_button = browser.find_element(
        By.XPATH,
        f"//ul[@id='portal-globalnav']/li[contains(@class, '{menu_button_class}')]/a"
    )
    try:
        menu_button.click()
    except ElementClickInterceptedException:
        browser.execute_script("arguments[0].click();", menu_button)


@when('I open form "{form_name}"')
def step_impl(context: behave.runner.Context, form_name: str) -> None:
    context.execute_steps(f'Given I opened form "{form_name}"')


@then('I should be on detail page of {} "{item_name}"')
def step_impl(context: behave.runner.Context, _, item_name: str) -> None:
    browser: WebDriver = context.selenium

    main_heading = browser.find_element(By.XPATH, "//h1[@class='documentFirstHeading']")
    assert main_heading.text.strip() == item_name


@then('{item_type} "{item_name}" should be visible for {user_type}')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str, user_type: str) -> None:
    browser: WebDriver = context.selenium

    # Become correct user
    if user_type == "user with reviewing privileges":
        context.execute_steps('When I log in as user with privileges to review Tools')
    elif user_type == "not logged in user":
        context.execute_steps('When I log out')
    else:
        raise NotImplementedError

    # Bad item's name (or forgotten creation in current scenario - use: Given I have {item_type} "{item_name}"
    if item_name not in context.urls:
        raise ValueError(f"{item_type} {item_name} isn't known in current scenario")

    # Go to item's detail page
    browser.get(context.urls[item_name])

    # When the user hasn't permissions, system changes URL to error page
    assert browser.current_url == context.urls[item_name]


@when('I delete the {item_type} "{item_name}"')
def step_impl(context: behave.runner.Context, item_type: str, item_name: str) -> None:
    browser: WebDriver = context.selenium

    # Bad item's name (or forgotten creation in current scenario - use: Given I have {item_type} "{item_name}"
    if item_name not in context.urls:
        raise ValueError(f"{item_type} {item_name} isn't known in current scenario")

    # Move to detail of the item
    browser.get(context.urls[item_name])

    # Open Actions menu
    menu_button = browser.find_element(By.XPATH, "//li[@id='plone-contentmenu-actions']/a")
    javascript_click(browser, menu_button)

    # Open delete dialog
    open_dialog_button = browser.find_element(By.ID, "plone-contentmenu-actions-delete")
    open_dialog_button.click()

    # Confirm dialog
    delete_button = browser.find_element(By.ID, "form-buttons-Delete")
    browser.execute_script("arguments[0].click();", delete_button)


@then('{} "{item_name}" should not be contained in "{section_name}"')
def step_impl(context: behave.runner.Context, _, item_name: str, section_name: str) -> None:
    browser: WebDriver = context.selenium

    if section_name == "Tools":
        selected_items_box_id = "form-widgets-tools"
        selected_item_name_class = "contenttype-tool state-private url"
    elif section_name == "Standards":
        selected_items_box_id = "form-widgets-standards"
        selected_item_name_class = "contenttype-standards state-private url"
    else:
        raise NotImplementedError

    try:
        selected_items_box = browser.find_element(By.ID, selected_items_box_id)

        selected_items: list[WebElement] = selected_items_box.find_elements(By.CLASS_NAME, selected_item_name_class)

        for item in selected_items:
            if item.text.strip() == item_name:
                break
        else:
            assert False
    except NoSuchElementException:
        # When no tool is selected, box for tools isn't in HTML at all, so this test ends successfully
        assert True


@then('{} "{item_name}" should be in "{section_name}"')
def step_impl(context: behave.runner.Context, _, item_name: str, section_name: str) -> None:
    # It is just negation of: {} "{item_name}" should not be contained in "{section_name}"
    try:
        context.execute_steps('{} "{item_name}" should not be contained in "{section_name}"')

        assert False
    except AssertionError:
        assert True
