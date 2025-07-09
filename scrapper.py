from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from pathlib import Path
import requests
from tqdm import tqdm

driver = uc.Chrome()
driver.implicitly_wait(2)

# Login
driver.get("https://www.sports-tracker.com/login")

print(f'\nYou have 30 seconds to login now.')
print(f'\t1. Enter your credentials.')
print(f'\t2. Click LOGIN.')
print(f'\t3. Click ACCEPT ALL at cookiees baner.')
print(f'\t4. Click LOGIN.')
print(f'\t5. Wait for script.')

time.sleep(20)

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

token = driver.execute_script('return window.localStorage.getItem("sessionkey");')
all_elems = driver.find_elements(by=By.CSS_SELECTOR, value='a')

identificators = []
for elem in all_elems:
    if elem != None:
        href = elem.get_attribute('href')
        if href != None:
            if '/workout/' in href:
                identificators.append(href[href.rfind('/')+1:])

driver.close()

# Download all GPX files
save_path = Path('datasets/GPXs')
save_path.mkdir(parents=True, exist_ok=True)

print(f'\nDownloading workouts')

for id in tqdm(identificators):
    url = f'https://api.sports-tracker.com/apiserver/v1/workout/exportGpx/{id}?token={token}'

    response = requests.get(url)

    with open(save_path / f'{id}.gpx', 'wb') as f:
        f.write(response.content)

print('Workouts scrapped')
