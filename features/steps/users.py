import behave.runner
from behave import *
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from helpers import javascript_click


@given('I am logged in as user with privileges to {privilege}')
def step_impl(context: behave.runner.Context, privilege: str) -> None:
    browser: WebDriver = context.selenium

    browser.get(f"{context.url}/login")

    # 2nd variant - not works every time, because it is a HTML link with href instead of `javascript:void(0);`,
    # so sometimes it loads this page, too. As a simple solution, the page is loaded every time for to be
    # sure what form will be used
    # open_form_button = browser.find_element(By.ID, "personaltools-login")
    # open_form_button.click()

    login_form = browser.find_element(By.XPATH, "//article[@id='content']/div[@id='login-form']/form")

    # 2nd variant needs different XPATH to access the form

    if "manage" in privilege:
        login = "itsadmin"
        password = "itsadmin"
    elif "review" in privilege:
        login = "itsreviewer"
        password = "itsreviewer"
    else:
        raise NotImplementedError

    login_input = login_form.find_element(By.ID, "__ac_name")
    login_input.send_keys(login)

    password_input = login_form.find_element(By.ID, "__ac_password")
    password_input.send_keys(password)

    login_button = login_form.find_element(By.XPATH, "//input[@id='buttons-login']")
    login_button.click()


@when('I log in as user with privileges to {privilege}')
def step_impl(context: behave.runner.Context, privilege: str) -> None:
    context.execute_steps(f'''
        When I log out
        Given I am logged in as user with privileges to {privilege}
    ''')


@when('I log out')
def step_impl(context: behave.runner.Context) -> None:
    browser: WebDriver = context.selenium

    try:
        menu_button = browser.find_element(By.ID, "portal-personaltools")
        javascript_click(browser, menu_button)
    except NoSuchElementException:
        # No user is logged in
        return

    logout_button = browser.find_element(By.ID, "personaltools-logout")
    logout_button.click()
