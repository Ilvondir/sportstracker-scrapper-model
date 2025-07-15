from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
from pathlib import Path
import requests
from tqdm import tqdm
import pandas as pd

driver = uc.Chrome()
driver.implicitly_wait(2)

# Login
driver.get('https://www.sports-tracker.com/login')

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

urls = []

for elem in all_elems:
    if elem != None:
        href = elem.get_attribute('href')
        if href != None:
            if '/workout/' in href:
                urls.append(href)


# Collect data from workouts
dataset = []
columns = ['Duration', 'Distance', 'Energy', 'Avg. speed', 'Max. speed', 'Steps']

for url in urls:
    record = []

    driver.get(url)
    time.sleep(.5)

    stats = driver.find_elements(by=By.CSS_SELECTOR, value='.workout-facts li')

    for column in columns:
        found = False
        for stat in stats:
            if column in stat.text:
                record.append(stat.find_element(by=By.TAG_NAME, value='em').text.strip())
                found = True
                break
        if not found:
            record.append('')

    found = False
    for stat in stats:
        if 'Ascent / Descent' in stat.text:
            record.extend(map(str.strip, stat.find_element(by=By.TAG_NAME, value='em').text[:-1].split('/')))
            found = True
            break
    if not found:
        record.extend(['', ''])

    label = driver.find_element(by=By.CSS_SELECTOR, value='.workout-facts .activity-name').text

    if any(elem != '' for elem in record):
        record.append(label)
        record.insert(0, url[url.rfind('/')+1:])
        dataset.append(record)

driver.close()

root = Path('datasets')
root.mkdir(parents=True, exist_ok=True)

columns.insert(0, 'ID')
columns.extend(['Ascent', 'Descent', 'Label'])

data = pd.DataFrame(dataset, columns=columns)
data.to_csv(root / 'workouts.csv', index=False)

print('Plain data scrapped')

# Download GPX files
save_path = root / 'GPXs'
save_path.mkdir(parents=True, exist_ok=True)

print(f'\nScraping workouts')

for link in tqdm(urls):
    id = link[link.rfind('/')+1:]
    url = f'https://api.sports-tracker.com/apiserver/v1/workout/exportGpx/{id}?token={token}'
    response = requests.get(url)
    with open(save_path / f'{id}.gpx', 'wb') as f:
        f.write(response.content)

print('Workouts scrapped')
