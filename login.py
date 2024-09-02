from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set your LinkedIn credentials
username = ''
password = ''

# Initialize Chrome WebDriver
driver = webdriver.Chrome()  # Ensure 'chromedriver' is in your PATH or provide the full path

# Open LinkedIn login page
driver.get('https://www.linkedin.com/login')

# Wait for the page to load
time.sleep(3)

# Locate and fill the username and password fields
email_field = driver.find_element(By.ID, 'username')
password_field = driver.find_element(By.ID, 'password')

email_field.send_keys(username)
password_field.send_keys(password)

# Submit the login form
login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
login_button.click()

# Wait for login to complete and the next page to load
time.sleep(5)

# Directly navigate to the followers page URL
followers_url = "https://www.linkedin.com/mynetwork/network-manager/people-follow/followers/"
driver.get(followers_url)

# Wait for the followers page to load
time.sleep(5)

# Scroll down to load more followers (if necessary)
scroll_pause_time = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(scroll_pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Extract the names of followers using a more general XPath
try:
    # Wait for the elements to be visible
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//span[contains(@class, "artdeco-entity-lockup__title")]//a')))

    # Corrected XPath to locate follower names and profile links
    followers_elements = driver.find_elements(By.XPATH, '//span[contains(@class, "artdeco-entity-lockup__title")]//a')

    # Print the names of followers
    for follower in followers_elements:
        print(follower.text, follower.get_attribute('href'))

except Exception as e:
    print("Error extracting followers' names:", e)

# Close the browser
driver.quit()
