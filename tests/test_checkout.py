import allure
from selenium.webdriver.common.by import By
import pytest

BASE_URL = "https://www.saucedemo.com"

@allure.feature("Checkout Process")
@allure.story("User completes checkout successfully")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.parametrize("username, password", [("standard_user", "secret_sauce")])
def test_checkout_process(driver, username, password):
    with allure.step("Open Login Page"):
        driver.get(BASE_URL)
    
    with allure.step("Enter Login Credentials"):
        driver.find_element(By.ID, "user-name").send_keys(username)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.ID, "login-button").click()
        
    with allure.step("Add Product to Cart"):
        driver.find_element(By.CLASS_NAME, "inventory_item").find_element(By.CLASS_NAME, "btn_inventory").click()
        driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    with allure.step("Proceed to Checkout"):
        driver.find_element(By.ID, "checkout").click()
        driver.find_element(By.ID, "first-name").send_keys("John")
        driver.find_element(By.ID, "last-name").send_keys("Doe")
        driver.find_element(By.ID, "postal-code").send_keys("12345")
        driver.find_element(By.ID, "continue").click()
    
    with allure.step("Complete Purchase"):
        driver.find_element(By.ID, "finish").click()

    with allure.step("Verify Success Message"):
        success_message = driver.find_element(By.CLASS_NAME, "complete-header").text
        assert success_message == "Thank you for your order!"
    
    allure.attach(driver.get_screenshot_as_png(), name="checkout_screenshot", attachment_type=allure.attachment_type.PNG)