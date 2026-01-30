from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import unittest
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC


class TestFormFill(unittest.TestCase):
    def setUp(self):
        """Initialize the WebDriver before each test."""
        self.driver = webdriver.Firefox(service=Service(), options=Options())
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def test_radio_buttons(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.tutorialspoint.com/selenium/practice/radio-button.php")
        time.sleep(2)

        # Locating elements
        radio_button_yes = driver.find_element(By.XPATH, "//input[@value='igottwo']")
        radio_button_impressive = driver.find_element(By.XPATH, "//input[@value='igotthree']")
        radio_button_no = driver.find_element(By.XPATH, "//div[@class='col-md-8 col-lg-8 col-xl-8']//div[5]")


        # Test 1: Choosing Yes radio button
        radio_button_yes.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, "check"), "Yes"))
        resulting_text = driver.find_element(By.ID, "check").text
        assert "You have checked Yes" in resulting_text
        print(f"✅ Test 1 passed: {resulting_text}")

        # Test 2. Choosing Impressive radio button
        radio_button_impressive.click()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.text_to_be_present_in_element((By.ID, "check1"), "Impressive"))
        resulting_text_2 = driver.find_element(By.ID, "check1").text
        assert "You have checked Impressive" in resulting_text_2
        print(f"✅ Test 2 passed: {resulting_text_2}")

        # Test 3. Choosing No radio button
        radio_button_no.click()
        assert radio_button_no.is_selected() == False
        print(f"✅ Test 2 passed: There is no text")
        print("\n✅ All tests are passed!")

        #driver.save_screenshot("radio_buttons_tests.png")

if __name__ == "__main__":
     unittest.main()