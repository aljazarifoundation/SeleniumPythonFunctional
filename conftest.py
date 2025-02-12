import pytest
import allure
import os
import getpass
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def take_screenshot(driver, scenario_name, step_name, status="pass"):
    """
    Take a screenshot with scenario and step information
    """
    try:
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        scenario_name = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in scenario_name)
        step_name = "".join(c if c.isalnum() or c in ['-', '_'] else '_' for c in step_name)
        
        screenshot_name = f"{scenario_name}_{step_name}_{status}_{timestamp}.png"
        screenshot_path = os.path.join("screenshots", screenshot_name)
        os.makedirs("screenshots", exist_ok=True)
        
        driver.save_screenshot(screenshot_path)
        allure.attach.file(
            screenshot_path,
            name=screenshot_name,
            attachment_type=allure.attachment_type.PNG
        )
        print(f"Screenshot saved: {screenshot_path}")
    except Exception as e:
        print(f"Failed to take screenshot: {str(e)}")

@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    window_size = request.config.getoption("--window-size")
    implicit_wait = request.config.getoption("--implicit-wait")
    
    try:
        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument('--start-maximized')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            driver = webdriver.Chrome(options=options)
            
        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Firefox(options=options)
            
        elif browser_name == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless")
            driver = webdriver.Edge(options=options)
            
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        if window_size:
            width, height = map(int, window_size.split('x'))
            driver.set_window_size(width, height)
        else:
            driver.maximize_window()
        
        driver.implicitly_wait(implicit_wait)
        print(f"Browser started: {browser_name}")
        
        yield driver
        
        driver.quit()
        print("Browser closed")
            
    except Exception as e:
        print(f"Error setting up browser: {str(e)}")
        raise

def pytest_bdd_after_step(request, feature, scenario, step, step_func, step_func_args):
    """Take screenshot after each step if enabled"""
    if request.config.getoption("--screenshots"):
        try:
            if hasattr(request, "getfixturevalue"):
                browser = request.getfixturevalue("browser")
                take_screenshot(browser, scenario.name, step.name)
        except Exception as e:
            print(f"Failed to capture step screenshot: {str(e)}")

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    
    if rep.when == "call" and rep.failed:
        try:
            if "browser" in item.funcargs and item.config.getoption("--screenshots"):
                driver = item.funcargs["browser"]
                scenario_name = item.function.__name__
                take_screenshot(driver, scenario_name, "test_failure", "failed")
        except Exception as e:
            print(f"Failed to capture error screenshot: {str(e)}")
    
    setattr(item, f"rep_{rep.when}", rep)

def pytest_bdd_step_error(request, feature, scenario, step, step_func, step_func_args, exception):
    """Take screenshot on step failure if enabled"""
    if request.config.getoption("--screenshots"):
        try:
            if hasattr(request, "getfixturevalue"):
                browser = request.getfixturevalue("browser")
                take_screenshot(browser, scenario.name, f"error_{step.name}", "failed")
        except Exception as e:
            print(f"Failed to capture step error screenshot: {str(e)}")

@pytest.fixture(scope='session', autouse=True)
def setup_allure_environment(request):
    # Get configuration from command line options
    base_url = request.config.getoption("--base-url")
    browser = request.config.getoption("--browser")
    environment = request.config.getoption("--test-env")
    tester = request.config.getoption("--tester") or getpass.getuser()
    timezone_offset = request.config.getoption("--timezone-offset")

    # Calculate current time with timezone offset
    current_time = datetime.utcnow() + timedelta(hours=int(timezone_offset))
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

    env_info = {
        "Base URL": base_url,
        "Browser": browser,
        "Environment": environment,
        "Tester": tester,
        "Date": formatted_time,
        "Headless": str(request.config.getoption("--headless")),
        "Window Size": request.config.getoption("--window-size")
    }

    os.makedirs('allure-results', exist_ok=True)
    
    with open('allure-results/environment.properties', 'w') as f:
        f.writelines(f'{k}={v}\n' for k, v in env_info.items())

def pytest_addoption(parser):
    # Browser configuration options
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on. Options: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--window-size",
        action="store",
        default="1920x1080",
        help="Set the browser window size. Format: WIDTHxHEIGHT"
    )
    parser.addoption(
        "--implicit-wait",
        action="store",
        type=int,
        default=10,
        help="Set implicit wait time in seconds"
    )
    parser.addoption(
        "--screenshots",
        action="store_true",
        default=False,
        help="Enable or disable taking screenshots during test execution"
    )

    # Allure environment configuration options
    parser.addoption(
        "--base-url",
        action="store",
        default="https://www.saucedemo.com",
        help="Base URL of the application"
    )
    parser.addoption(
        "--test-env",
        action="store",
        default="QA",
        help="Test environment (e.g., QA, Staging, Production)"
    )
    parser.addoption(
        "--tester",
        action="store",
        default=None,
        help="Tester name (defaults to current user if not specified)"
    )
    parser.addoption(
        "--timezone-offset",
        action="store",
        default="7",
        help="Timezone offset from UTC in hours (e.g., 7 for Jakarta/UTC+7)"
    )

def pytest_configure(config):
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')