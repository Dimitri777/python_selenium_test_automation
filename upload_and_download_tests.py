import os
import time
from pathlib import Path
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class TestUploadDownload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path.home() / "Downloads" / "selenium_tests"
        cls.test_dir.mkdir(exist_ok=True)

        # Create test files
        cls.test_file = cls.test_dir / "test_upload.txt"
        with open(cls.test_file, 'w') as f:
            f.write("Test content for upload")

        cls.test_image = cls.test_dir / "sampleFile.jpeg"
        with open(cls.test_image, 'wb') as f:
            f.write(b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01')

        # Firefox options
        options = Options()
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", str(cls.test_dir))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/octet-stream,text/plain,image/jpeg,application/pdf")

        cls.driver = webdriver.Firefox(options=options)
        cls.driver.maximize_window()
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # Clean test files
        for file_path in [cls.test_file, cls.test_image]:
            if file_path.exists():
                file_path.unlink()
        # Clean directory if empty
        try:
            if cls.test_dir.exists() and not any(cls.test_dir.iterdir()):
                cls.test_dir.rmdir()
        except:
            pass

    def test_download(self):
        """Test file download functionality"""
        print("Testing file download...")
        self.driver.get("https://www.tutorialspoint.com/selenium/practice/upload-download.php")

        # Wait for page and get files before download
        self.wait.until(EC.title_contains("Selenium"))
        files_before = set(self.test_dir.glob("*"))

        # Find and click download button
        download_btn = self.wait.until(
            EC.element_to_be_clickable((By.ID, "downloadButton"))
        )
        download_btn.click()

        # Wait for download (increase wait time if needed)
        time.sleep(5)

        # Check new file
        files_after = set(self.test_dir.glob("*"))
        new_files = files_after - files_before

        self.assertTrue(len(new_files) > 0, "No file was downloaded")
        downloaded_file = next(iter(new_files))
        self.assertTrue(downloaded_file.stat().st_size > 0, "Downloaded file is empty")
        print(f"✓ Downloaded: {downloaded_file.name}")

    def test_upload_text(self):
        """Test text file upload"""
        print("\nTesting text file upload...")
        self.driver.get("https://www.tutorialspoint.com/selenium/practice/upload-download.php")

        # Wait for upload input
        upload_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "uploadFile"))
        )

        # Upload file
        upload_input.send_keys(str(self.test_file))
        time.sleep(3)

        # Check for confirmation - Based on HTML you provided, there might not be uploadedFilePath element
        # Try different ways to confirm upload

        # Option 1: Check if file is selected in input (value attribute)
        file_value = upload_input.get_attribute("value")
        if file_value:
            print(f"✓ File selected: {file_value}")
            self.assertIn(self.test_file.name, file_value)
        else:
            # Option 2: Look for any confirmation message
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            self.assertIn(self.test_file.name, page_text)
            print(f"✓ File confirmed in page text")

        # Option 3: Check if label shows filename
        try:
            label = self.driver.find_element(By.CSS_SELECTOR, "label.form-file-label")
            if self.test_file.name in label.text:
                print(f"✓ File shown in label: {label.text}")
        except:
            pass

    def test_upload_image(self):
        """Test image file upload"""
        print("\nTesting image file upload...")
        self.driver.get("https://www.tutorialspoint.com/selenium/practice/upload-download.php")

        # Wait for upload input
        upload_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "uploadFile"))
        )

        # Clear any previous selection
        self.driver.execute_script("arguments[0].value = '';", upload_input)
        time.sleep(1)

        # Upload image
        upload_input.send_keys(str(self.test_image))
        time.sleep(3)

        # Check confirmation - same as text upload test
        file_value = upload_input.get_attribute("value")
        self.assertTrue(file_value, "No file appears to be selected")

        if file_value:
            print(f"✓ Image selected: {file_value}")
            self.assertIn(self.test_image.name, file_value)
        else:
            # Fallback to page text check
            page_text = self.driver.find_element(By.TAG_NAME, "body").text
            self.assertIn(self.test_image.name, page_text)
            print(f"✓ Image confirmed in page text")

    def test_upload_and_download_combined(self):
        """Test both upload and download on same page"""
        print("\nTesting combined upload and download...")
        self.driver.get("https://www.tutorialspoint.com/selenium/practice/upload-download.php")

        # Test upload first
        upload_input = self.wait.until(
            EC.presence_of_element_located((By.ID, "uploadFile"))
        )
        upload_input.send_keys(str(self.test_file))
        time.sleep(2)

        # Verify upload
        file_value = upload_input.get_attribute("value")
        self.assertTrue(file_value, "Upload failed")

        # Test download
        files_before = set(self.test_dir.glob("*"))
        download_btn = self.driver.find_element(By.ID, "downloadButton")
        download_btn.click()
        time.sleep(5)

        # Verify download
        files_after = set(self.test_dir.glob("*"))
        new_files = files_after - files_before
        self.assertTrue(len(new_files) > 0, "Download failed after upload")
        print("✓ Combined test passed")


if __name__ == "__main__":
    # Run tests with more details
    unittest.main(verbosity=2, failfast=True)