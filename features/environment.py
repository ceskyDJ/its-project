import random
import sys
from time import sleep

from behave import fixture, use_fixture, runner
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.remote.webdriver import WebDriver


@fixture
def init_selenium(context: runner.Context) -> None:
    # -- SETUP-FIXTURE PART:
    if "-w" in sys.argv or "--wip" in sys.argv:
        context.selenium = webdriver.Firefox()
    else:
        try:
            context.selenium = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX)
        except WebDriverException:
            context.selenium = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)

    context.selenium.implicitly_wait(15)

    yield context.selenium

    # -- CLEANUP-FIXTURE PART:
    context.selenium.quit()


@fixture
def load_main_page(context: runner.Context) -> WebDriver:
    browser: WebDriver = context.selenium

    # -- SETUP-FIXTURE PART:
    if "-w" in sys.argv or "--wip" in sys.argv:
        browser.get("http://localhost:8080/repo")
    else:
        browser.get("http://valu3s:8080/repo")

    yield browser

    # -- CLEANUP-FIXTURE PART:
    browser.delete_all_cookies()


def before_all(context: runner.Context) -> None:
    # Set fix seed random (it will generate always the same values)
    random.seed(1)

    use_fixture(init_selenium, context)


def after_all(_) -> None:
    if "-w" in sys.argv or "--wip" in sys.argv:
        sleep(10)


def before_scenario(context: runner.Context, _) -> None:
    use_fixture(load_main_page, context)
