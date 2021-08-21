import time

import selenium.common.exceptions
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import io

default_wait_time = 15


def press_arrow():
    arrow = WebDriverWait(driver, default_wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//a[text() = 'Next']")))
    arrow.click()


def parse_text():
    try:
        text = WebDriverWait(driver, default_wait_time).until(
            EC.presence_of_element_located((By.XPATH, "// li[ @ role = 'menuitem'] / div / div / div / span")))
        text_to_file(text.text)
    except selenium.common.exceptions.TimeoutException:
        text_to_file('')
        return


def text_to_file(text):
    f = io.open('text.txt', mode="a", encoding="utf-8")
    f.write(text + ' ')


login_data = open('account.txt').read().split('\n')
names = open('names.txt').read().split('\n')
login_wait_time = 30
driver = webdriver.Chrome('chromedriver.exe')
driver.get("https://www.instagram.com")
username = WebDriverWait(driver, login_wait_time).until(
    EC.presence_of_element_located((By.XPATH, "//input[@name='username']"))
)
time.sleep(5)
username.send_keys(login_data[0])
passw = driver.find_element_by_xpath("//input[@name='password']")
time.sleep(5)
passw.send_keys(login_data[1])
log_in_button = driver.find_element_by_xpath("//button[@type = 'submit']")
time.sleep(2)
log_in_button.click()
try:
    not_now_button = WebDriverWait(driver, login_wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//button[1 and text() = 'Not Now']")))
    not_now_button.click()
except selenium.common.exceptions.TimeoutException:
    pass
try:
    not_now_button = WebDriverWait(driver, login_wait_time).until(
        EC.presence_of_element_located((By.XPATH, "//button[1 and text() = 'Not Now']")))
    not_now_button.click()  # there are might be two pop-up messages with not now button
except selenium.common.exceptions.TimeoutException:
    pass
for name in names:
    driver.get("https://www.instagram.com/" + name)
    try:
        photo = WebDriverWait(driver, default_wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//article/div/div/div/div/a")))
        photo.click()
    except selenium.common.exceptions.TimeoutException:
        pass
    while True:
        parse_text()
        try:
            time.sleep(3)
            press_arrow()
        except selenium.common.exceptions.TimeoutException:
            break
