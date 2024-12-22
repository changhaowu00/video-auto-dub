from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os

# Replace with your OpenAI credentials
EMAIL = "your_email@example.com"
PASSWORD = "your_password"

# Path to your local WebDriver (e.g., ChromeDriver)
#CHROMEDRIVER_PATH = "/mnt/c/Users/chang/Downloads/chromedriver-linux64/chromedriver"  # Update with the correct path
CHROMEDRIVER_PATH = "C:/Users/chang/Downloads/chromedriver-win64/chromedriver.exe"

# Initialize the WebDriver (local driver setup)
# Set up Chrome options
chrome_options = Options()
# chrome_options.add_argument("--start-maximized")  # Open browser in maximized mode
# chrome_options.add_argument("--disable-infobars")  # Disable the info bar
# chrome_options.add_argument("--disable-extensions")  # Disable extensions
# chrome_options.add_argument("--headless")  # Run in headless mode (optional)
# chrome_options.add_argument("--no-sandbox")  # Sandbox is needed in some environments
# chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome resource issues

# Set up the WebDriver
service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.google.com")
print(driver.title)



# Step 1: Open OpenAI's login page
driver.get("https://chatgpt.com/c/67680e8f-ecdc-8007-9600-f80857bd66b2")
while True:
    pass

