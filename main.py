from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def print_current_info():
    current_time = "2025-02-10 04:20:49"
    current_user = "DianPermana"
    
    print(f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {current_time}")
    print(f"Current User's Login: {current_user}")

def test_saucedemo_login():
    # Setup webdriver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    
    try:
        # Open website
        print("\nStarting login test...")
        driver.get("https://www.saucedemo.com/")
        
        # Login steps
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        
        # Verify login success
        if "inventory.html" in driver.current_url:
            print("Test PASSED ✅ - Successfully logged in and reached inventory page")
        else:
            print("Test FAILED ❌ - Could not reach inventory page")

        time.sleep(60)
            
    except Exception as e:
        print(f"Test FAILED ❌ - An error occurred: {str(e)}")
        
    finally:
        # Cleanup
        driver.quit()

if __name__ == "__main__":
    print_current_info()
    test_saucedemo_login()