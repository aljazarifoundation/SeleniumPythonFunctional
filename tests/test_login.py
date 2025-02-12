import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest

BASE_URL = "https://www.saucedemo.com"

@allure.epic("SauceDemo Login Tests")
@allure.feature("User Authentication")
@allure.story("Valid Login")
@pytest.mark.functional
def test_valid_login(driver):
    with allure.step("Open SauceDemo login page"):
        driver.get(BASE_URL)

    with allure.step("Enter valid username and password"):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("Click login button"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("Verify successful login"):
        assert "/inventory.html" in driver.current_url

@allure.feature("User Authentication")
@allure.story("Invalid Login")
@pytest.mark.functional
def test_invalid_login(driver):
    with allure.step("Open SauceDemo login page"):
        driver.get(BASE_URL)

    with allure.step("Enter invalid username and password"):
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("wrong_password")

    with allure.step("Click login button"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("Verify error message"):
        error_msg = driver.find_element(By.CLASS_NAME, "error-message-container").text
        assert "Username and password do not match" in error_msg

@allure.feature("User Authentication")
@allure.story("Locked Out User")
@pytest.mark.functional
def test_locked_out_user(driver):
    with allure.step("Open SauceDemo login page"):
        driver.get(BASE_URL)

    with allure.step("Enter locked-out user credentials"):
        driver.find_element(By.ID, "user-name").send_keys("locked_out_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")

    with allure.step("Click login button"):
        driver.find_element(By.ID, "login-button").click()

    with allure.step("Verify error message appears"):
        error_message = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']").text
        assert "Sorry, this user has been locked out." in error_message
