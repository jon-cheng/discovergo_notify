import pytest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.discovergo_notify.scrape import Credentials, WebDriverFactory, Scraper

# Test for Credentials class
@patch("os.getenv")
def test_missing_credentials(mock_getenv):
    """Test that missing credentials raise a ValueError."""
    mock_getenv.side_effect = lambda key: None  # Simulate missing environment variables
    credentials = Credentials()
    with pytest.raises(ValueError, match="Missing credentials"):
        credentials.validate()

@patch("os.getenv")
def test_valid_credentials(mock_getenv):
    """Test that valid credentials are loaded correctly."""
    mock_getenv.side_effect = lambda key: "test_value" if key in ["ePASSPatronNumber", "ePASSPatronPassword"] else None
    credentials = Credentials()
    credentials.validate()
    assert credentials.username == "test_value"
    assert credentials.password == "test_value"

# Test for WebDriverFactory class
@patch("selenium.webdriver.Chrome")
def test_webdriver_initialization(mock_chrome):
    """Test that WebDriverFactory creates a WebDriver instance."""
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    driver = WebDriverFactory.create_driver()
    assert driver == mock_driver

@patch("selenium.webdriver.Chrome")
def test_webdriver_initialization_failure(mock_chrome):
    """Test that WebDriverFactory handles driver creation errors."""
    mock_chrome.side_effect = Exception("WebDriver initialization failed")
    with pytest.raises(Exception, match="WebDriver initialization failed"):
        WebDriverFactory.create_driver()

# Test for Scraper class
@patch("selenium.webdriver.Chrome")
@patch("selenium.webdriver.support.ui.WebDriverWait.until")
def test_scraper_login_success(mock_wait_until, mock_chrome):
    """Test that Scraper successfully logs in."""
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    mock_wait_until.return_value = MagicMock()  # Mock the login fields

    credentials = Credentials()
    credentials.username = "test_user"
    credentials.password = "test_pass"

    scraper = Scraper("https://example.com", credentials)
    driver = scraper.start()

    # Verify that login fields were interacted with
    mock_driver.get.assert_called_once_with("https://example.com")
    assert mock_wait_until.call_count == 2  # Username and password fields
    driver.quit()

@patch("selenium.webdriver.Chrome")
@patch("selenium.webdriver.support.ui.WebDriverWait.until")
def test_scraper_login_failure(mock_wait_until, mock_chrome):
    """Test that Scraper raises an error if login fields are not found."""
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    mock_wait_until.side_effect = TimeoutException("Login field not found")

    credentials = Credentials()
    credentials.username = "test_user"
    credentials.password = "test_pass"

    scraper = Scraper("https://example.com", credentials)
    with pytest.raises(TimeoutException, match="Login field not found"):
        scraper.start()

@patch("selenium.webdriver.Chrome")
@patch("selenium.webdriver.support.ui.WebDriverWait.until")
def test_scraper_page_load_timeout(mock_wait_until, mock_chrome):
    """Test that Scraper handles timeouts when waiting for the page to load."""
    mock_driver = MagicMock()
    mock_chrome.return_value = mock_driver
    mock_wait_until.side_effect = TimeoutException("Page load timeout")

    credentials = Credentials()
    credentials.username = "test_user"
    credentials.password = "test_pass"

    scraper = Scraper("https://example.com", credentials)
    with pytest.raises(TimeoutException, match="Page load timeout"):
        scraper.start()