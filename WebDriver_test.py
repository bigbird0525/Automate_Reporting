import os, time
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import date, timedelta
from bs4 import BeautifulSoup as bsoup
import DB

cred = {'Advertiser':'Ad.net','Platform':'LKQD','User':'melissaitoappthis','Password':'appthis4321!'}
browser = webdriver.Firefox()
wait = WebDriverWait(browser, 30)
browser.get("https://ui.lkqd.com/login")
userElement = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
userElement.send_keys(cred.pop('User'))
passElement = browser.find_element_by_id("password")
passElement.send_keys(cred.pop('Password'))
browser.find_element_by_class_name("btn.btn-primary").click()
time.sleep(1)
