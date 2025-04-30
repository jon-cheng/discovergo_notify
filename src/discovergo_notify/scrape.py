import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from loguru import logger
from dotenv import load_dotenv

load_dotenv()

TARGET_URL = "https://alamedafree.discoverandgo.net/"


class Credentials:
    """Class to manage user credentials. Load env vars from .env file"""

    def __init__(self):
        self.username = os.getenv("ePASSPatronNumber") 
        self.password = os.getenv("ePASSPatronPassword")

    def validate(self):
        """Validate that credentials are loaded."""
        if not self.username or not self.password:
            raise ValueError(
                "Missing credentials. Ensure ePASSPatronNumber and ePASSPatronPassword are set in the environment."
            )


class WebDriverFactory:
    """Factory class to create and configure a Selenium WebDriver."""

    @staticmethod
    def create_driver(headless=True, window_size="1920,1080"):
        """Creates and returns a configured WebDriver instance."""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")  # Run in headless mode for ETLs
        options.add_argument(f"--window-size={window_size}")  # Set default window size
        return webdriver.Chrome(options=options)


class Scraper:
    """Class to handle the scraping logic."""

    def __init__(self, url, credentials, wait_time=30):
        self.url = url
        self.credentials = credentials
        self.wait_time = wait_time
        self.driver = WebDriverFactory.create_driver()

    def start(self):
        """Starts the scraping process."""
        self.driver.get(self.url)

        # Wait for login fields
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "ePASSPatronNumber"))
        )
        password_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "ePASSPatronPassword"))
        )

        # Log in using credentials
        username_field.send_keys(self.credentials.username)
        password_field.send_keys(self.credentials.password)
        password_field.send_keys(Keys.RETURN)

        # Wait for page load
        WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.ID, "ePASSAttractions"))
        )
        time.sleep(10)  # Give the page time to finish rendering

        return self.driver

    def close(self):
        """Closes the WebDriver."""
        self.driver.quit()


class PageNavigator:
    pass


class HTMLParser:
    pass


# Usage
if __name__ == "__main__":

    logger.info("Starting the scraping process...")

    credentials = Credentials()
    credentials.validate()

    scraper = Scraper(TARGET_URL, credentials)

    driver = None

    try:
        driver = scraper.start()

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # current attractions
        attractions = soup.find_all("span", class_="ePASSAttractionName")

        # Filter and print elements that match the specific text
        for attraction in attractions:
            print(attraction.text.strip())

        print(len(attractions), "attractions found.")

        # Perform scraping logic here...

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the driver
        scraper.close()
