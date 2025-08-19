from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Set up Chrome options (optional)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Uncomment if you want to run headless

# Set up the ChromeDriver service
service = Service(ChromeDriverManager().install())

# Initialize the WebDriver with the service and options
driver = webdriver.Chrome(service=service, options=chrome_options)

# Now you can use the driver to interact with the webpage
driver.get("https://talentedge.com/browse-courses")
print(driver.title)

# Don't forget to close the driver when done
driver.quit()
