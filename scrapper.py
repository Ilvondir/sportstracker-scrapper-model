from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
import undetected_chromedriver as uc
load_dotenv()

email = os.getenv('SPORTSTRACKER_EMAIL')
password = os.getenv('SPORTSTRACKER_PASSWORD')

driver = uc.Chrome()

# Login
driver.get("https://www.sports-tracker.com/login")

print('You have 30 seconds to login now.')
print(f'\t1. Enter your credentials: {email} {password}')
print(f'\t2. Click LOGIN.')
print(f'\t3. Click ACCEPT ALL at cookiees baner.')
print(f'\t4. Click LOGIN.')
print(f'\t5. Wait for script.')

time.sleep(30)

driver.implicitly_wait(2)

if False:
    email_field = driver.find_element(by=By.CSS_SELECTOR, value='input[type="text"].username')
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element(by=By.CSS_SELECTOR, value='input[type="password"].password')
    password_field.clear()
    password_field.send_keys(password)

    time.sleep(1)

    driver.find_element(by=By.CSS_SELECTOR, value='input[type="submit"].submit').click()




driver.close()