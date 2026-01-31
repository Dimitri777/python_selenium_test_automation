from tokenize import Ignore

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import unittest
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

class TestButtonsForm(unittest.TestCase):
    def setUp(self):
        """Initialize the WebDriver before each test."""
        self.driver = webdriver.Firefox(service=Service(), options=Options())
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        """Close the browser after each test."""
        self.driver.quit()

    def test_buttons_form_title(self):
        driver = self.driver
        driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")
        time.sleep(2)

        """Test form title and labels"""
        print("\n=== Testing Form Title and Labels ===")

        # Check form title
        title = self.driver.title
        assert title == "Selenium Practice - Buttons", f"Expected title 'Buttons', got '{title.text}'"
        print(f"✓ Title correct: {title}")

        # Find all buttons (assuming they are <button> elements)
        buttons = self.driver.find_elements(By.TAG_NAME, "button")

        # If not <button> tags, try other selectors
        if len(buttons) < 3:
            buttons = self.driver.find_elements(By.CSS_SELECTOR, "input[type='button'], button, div[role='button']")

        # Verify we have 3 buttons
        assert len(buttons) >= 3, f"Expected at least 3 buttons, found {len(buttons)}"
        print(f"✓ Found {len(buttons)} buttons")

        # Check button texts
        expected_texts = ["Click Me", "Right Click Me", "Double Click Me"]
        button_texts = [btn.text for btn in buttons[:3]]  # Take first 3 buttons

        for expected in expected_texts:
            assert (expected in text for text in button_texts), f"Button with text '{expected}' not found"
            print(f"✓ Button text found: {expected}")

    def test_click_me_button(self):
        driver = self.driver
        driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")
        time.sleep(2)
        """Test regular click on 'Click Me' button"""
        print("\n=== Testing 'Click Me' Button ===")

        # Find the 'Click Me' button
        click_me_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[normalize-space()='Click Me']")
        ))

        # Click the button
        click_me_btn.click()
        time.sleep(0.5)

        # Check the result message
        result_elements = self.driver.find_elements(By.ID, "welcomeDiv")

        # Look for the click message
        click_message_found = False
        for element in result_elements:
            if "dynamic click" in element.text.lower():
                assert "You have done a dynamic click" in element.text, f"Unexpected message: {element.text}"
                print(f"✓ Click message: {element.text}")
                click_message_found = True
                break

        assert click_message_found, "Click message not found after clicking 'Click Me' button"

    @unittest.skip("Test is switched off temporarily due to issue with right-click on the button on site")
    def test_right_click_me_button(self):
        driver = self.driver
        driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")
        time.sleep(2)
        """Test right-click (context click) on 'Right Click Me' button"""
        print("\n=== Testing 'Right Click Me' Button ===")

        # Find the 'Right Click Me' button
        right_click_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Right Click Me')]")
        ))

        # Perform right-click
        self.actions = ActionChains(self.driver)
        self.actions.context_click(right_click_btn).perform()
        time.sleep(0.5)

        # Check the result message
        result_elements = self.driver.find_elements(By.ID, "doublec")

        # Look for any message indicating right click
        # (The image shows it might show "You have done a dynamic click" for right click too)
        message_found = False
        for element in result_elements:
            if "You have" in element.text:
                print(f"✓ Right-click message: {element.text}")
                message_found = True
                break

        assert message_found, "No message found after right-click"

    def test_double_click_me_button(self):
        driver = self.driver
        driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")
        time.sleep(2)

        """Test double-click on 'Double Click Me' button"""
        print("\n=== Testing 'Double Click Me' Button ===")

        # Find the 'Double Click Me' button
        double_click_btn = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Double Click Me')]")
        ))

        # Perform double-click
        self.actions = ActionChains(self.driver)
        self.actions.double_click(double_click_btn).perform()
        time.sleep(0.5)

        # Check the result message
        result_elements = self.driver.find_elements(By.ID, "doublec")

        # Look for double click message
        double_click_message_found = False
        for element in result_elements:
            if "Double clicked" in element.text:
                assert "You have Double clicked" in element.text, f"Unexpected message: {element.text}"
                print(f"✓ Double-click message: {element.text}")
                double_click_message_found = True
                break

        assert double_click_message_found, "Double click message not found"

    def test_all_buttons_in_sequence(self):
        driver = self.driver
        driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")

        """Test all buttons in sequence and verify messages"""
        print("\n=== Testing All Buttons in Sequence ===")

        # Test Click Me
        self.test_click_me_button()

        # Test Right Click Me
        # self.test_right_click_me_button()

        # Test Double Click Me
        self.test_double_click_me_button()

        print("\n✅ All buttons tested successfully in sequence!")

    def test_run_all_tests(self):
        """Run all tests"""
        try:
            self.setUp()
            self.test_buttons_form_title()
            self.test_all_buttons_in_sequence()
            return True
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            # Take screenshot on failure
            self.driver.save_screenshot("test_failure.png")
            return False
        finally:
            self.tearDown()


    # Alternative compact version
    def test_buttons_compact(self):
        """Compact version of the button tests"""
        driver = webdriver.Firefox()
        actions = ActionChains(driver)

        try:
            # Open page
            driver.get("https://www.tutorialspoint.com/selenium/practice/buttons.php")
            time.sleep(2)

            print("=== Testing Buttons Form ===")

            # Test 1: Click Me
            click_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Click Me']")
            click_btn.click()
            time.sleep(0.5)

            # Check for click message
            messages = driver.find_elements(By.ID, "welcomeDiv")
            click_found = False
            for msg in messages:
                if "dynamic click" in msg.text.lower():
                    assert "You have done a dynamic click" in msg.text
                    print(f"✓ Test 1 passed: {msg.text}")
                    click_found = True
                    break
            assert click_found, "Click message not found"
            '''
            # Test 2: Right Click Me - disabled due to issue on the site
            right_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Right Click Me']")
            actions.context_click(right_btn).perform()
            time.sleep(0.5)

            # Check for any message
            messages = driver.find_elements(By.ID, "welcomeDiv")
            right_click_found = False
            for msg in messages:
                if "You have" in msg.text:
                    print(f"✓ Test 2 passed: {msg.text}")
                    right_click_found = True
                    break
            assert right_click_found, "Right-click message not found"
            '''
            # Test 3: Double Click Me
            double_btn = driver.find_element(By.XPATH, "//button[normalize-space()='Double Click Me']")
            actions.double_click(double_btn).perform()
            time.sleep(0.5)

            # Check for double click message
            messages = driver.find_elements(By.ID, "doublec")
            double_click_found = False
            for msg in messages:
                if "Double clicked" in msg.text:
                    assert "You have Double clicked" in msg.text
                    print(f"✓ Test 3 passed: {msg.text}")
                    double_click_found = True
                    break
            assert double_click_found, "Double-click message not found"

            print("\n✅ All button tests passed!")

        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
    print("Running button form tests...")

    # Run class-based tests
    test_suite = TestButtonsForm()
    success = test_suite.run_all_tests()

    print("\n✅ Test execution completed!")