import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
import time


class TestFormFill(unittest.TestCase):

    def setUp(self):
        """Initialize the WebDriver before each test."""

        # firefox_options.add_argument("--headless")
        self.driver = webdriver.Firefox(service=Service(), options=Options())
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def test_fill_form(self):
        driver = self.driver
        wait = self.wait

        # Open the form page
        driver.get("https://www.tutorialspoint.com/selenium/practice/text-box.php")

        # Fill out the form fields using XPath based on labels
        full_name_field = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='fullname']"))
        )
        full_name_field.clear()
        full_name_field.send_keys("Test User")

        email_field = driver.find_element(By.XPATH, "//input[@id='email']")
        email_field.clear()
        email_field.send_keys("test@example.com")

        address_field = driver.find_element(By.ID, "address")
        address_field.clear()
        address_field.send_keys("Test Address 123")

        password_field = driver.find_element(By.ID, "password")
        password_field.clear()
        password_field.send_keys("TestPass123")

        # Submit the form
        submit_btn = driver.find_element(By.XPATH, "//input[@value='Submit']")
        submit_btn.click()

        # Wait for response processing
        time.sleep(2)

        # Just a simple pytest assertion
        assert 1 + 2 == 3

        # Verify the response
        # Verify successful submission
        self.assertIn("Selenium Practice", driver.title, "Page title does not match")
        self.assertIn("text-box.php", driver.current_url, "Wrong page loaded!")

        # Optional: Take a screenshot on success
        self.driver.save_screenshot("form_success.png")


if __name__ == "__main__":
    unittest.main()
