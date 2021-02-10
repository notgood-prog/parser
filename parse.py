from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup 
import time
import pandas as pd
import re

driver = webdriver.Chrome('/Users/chromedriver')
driver.get("https://1xstavka.ru/results/")

wait = WebDriverWait(driver, 10)
element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'c-nav__item')))
driver.find_element_by_xpath('//*[@title="Волейбол"]').click()
driver.find_element_by_xpath('//*[@title="Развернуть все"]').click()
driver.find_element_by_xpath('//*[@class="vdp-datepicker c-filter-datepiker"]').click()
for i in range(71):
    driver.find_element_by_xpath('//*[@class="prev"]').click()
driver.find_element_by_xpath('//*[@id="router_app"]/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/span[14]').click()
time.sleep(5)
for i in range(15, 43):
    try:
        driver.find_element_by_xpath('//*[@class="vdp-datepicker c-filter-datepiker"]').click()
        driver.find_element_by_xpath(f'//*[@id="router_app"]/div/div[2]/div/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div[2]/div/span[{i}]').click()
        time.sleep(10)
        data = driver.page_source
        Html_file = open("fin","w")
        Html_file.write(data)
        Html_file.close()
        html_file = open("fin","r")
        contents = html_file.read()
        soup = BeautifulSoup(contents)
        Html_file.close()
        results = []
        matches_list = soup.find('div', {'class': 'c-games__item'})
        matches = matches_list.find_all('div', {'class': 'c-games__col'})
        for match in matches:
            name = match.find('div', {'class': 'c-games__name'})
            start_dt = match.find('div', {'class': 'c-games__date'}).text
            events_command = match.find('div', {'class': 'c-games__opponents u-dir-ltr'}).text
            events_score = match.find('div', {'class': 'c-games__results u-mla u-tar'}).text
            results.append({
                        'name': name,
                        'start_dt': start_dt,
                        'events_command': events_command,
                        'events_score': events_score
                        })
            full_df = pd.DataFrame(results)
            full_df['name'] = full_df.name.fillna(method = 'ffill')
            full_df['name'] = full_df.name.apply(lambda x: ' '.join(map(str, x)))
            full_df['name'] = full_df.name.apply(lambda x: x.replace('\n ', ''))
            full_df['start_dt'] = full_df.start_dt.apply(lambda x: x.replace('\n ', ''))
            full_df['events_command'] = full_df.events_command.apply(lambda x: x.replace('\n ', ''))
            full_df['events_score'] = full_df.events_score.apply(lambda x: x.replace('\n ', ''))
            full_df.name = full_df.name.str.strip()
            full_df.start_dt = full_df.start_dt.str.strip()
            full_df.events_command = full_df.events_command.str.strip()
            full_df.events_score = full_df.events_score.str.strip()
            full_df = full_df.drop_duplicates()
            full_df.to_csv('1x_dataset.csv', mode='a', header=False)
    except Exception as e:
        print(str(e))
        pass     

driver.close()
