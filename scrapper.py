from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import time
import undetected_chromedriver as uc
load_dotenv()

email = os.getenv('SPORTSTRACKER_EMAIL')
password = os.getenv('SPORTSTRACKER_PASSWORD')

driver = uc.Chrome()
driver.implicitly_wait(2)

# Login
driver.get("https://www.sports-tracker.com/login")

print('You have 30 seconds to login now.')
print(f'\t1. Enter your credentials: {email} {password}')
print(f'\t2. Click LOGIN.')
print(f'\t3. Click ACCEPT ALL at cookiees baner.')
print(f'\t4. Click LOGIN.')
print(f'\t5. Wait for script.')

time.sleep(15)

if False:
    email_field = driver.find_element(by=By.CSS_SELECTOR, value='input[type="text"].username')
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element(by=By.CSS_SELECTOR, value='input[type="password"].password')
    password_field.clear()
    password_field.send_keys(password)

    time.sleep(1)

    driver.find_element(by=By.CSS_SELECTOR, value='input[type="submit"].submit').click()


# Load all workouts
driver.find_element(by=By.CSS_SELECTOR, value='a[href="/diary"]').click()
time.sleep(1)
driver.find_elements(by=By.CLASS_NAME, value='tab')[1].click()
time.sleep(1)

while True:
    elem = driver.find_element(by=By.CLASS_NAME, value='show-more')

    if 'ng-hide' in elem.get_attribute('class'):
        break

    elem.click()
    time.sleep(0.5)

driver.close()

all_elems = driver.find_elements(by=By.CSS_SELECTOR, value='.diary-list__workout a')
identificators = [elem.get_attribute('href')[elem.get_attribute('href').rfind('/')+1:] for elem in all_elems]

# Download all GPX files