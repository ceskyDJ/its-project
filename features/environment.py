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
    browser.get(context.url)

    yield browser

    # -- CLEANUP-FIXTURE PART:
    browser.delete_all_cookies()


def before_all(context: runner.Context) -> None:
    # Set fix seed random (it will generate always the same values)
    random.seed(1)

    # Add root URL to context
    if "-w" in sys.argv or "--wip" in sys.argv:
        context.url = "http://localhost:8080/repo"
    else:
        context.url = "http://valu3s:8080/repo"

    use_fixture(init_selenium, context)


def after_all(_) -> None:
    if "-w" in sys.argv or "--wip" in sys.argv:
        sleep(10)


def before_scenario(context: runner.Context, _) -> None:
    # Prepare empty container for mapping names of created items with their URLs (names aren't unique)
    # It is the URL with view (/view), these pages are displayed after creating new item
    context.urls = dict()

    use_fixture(load_main_page, context)
