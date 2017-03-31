import os, time
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import date, timedelta
from bs4 import BeautifulSoup as bsoup
import DB

class Scraper_Exception(Exception):
    pass

class WebDriver_Exception(Exception):
    pass

class GetCredentials(object):

    def run(self, file):
        credentials = []
        dict_columns = ['Advertiser','Platform','User','Password']
        with open(os.getcwd() + "/" + file) as logins:
            reader = csv.reader(logins)
            for row in reader:
                cred_dict = dict(zip(dict_columns,row))
                credentials.append(cred_dict)
        return credentials

class LKQD_Scraper(Scraper_Exception):

    def scrapeData(self, browser):
        '''
        takes web driver object and scrapes page, returns list [impression, revenue]
        '''
        result_list = []
        soup = bsoup(browser.page_source, 'html.parser')
        try:
            row = soup.find_all('table')[0]
            impression = row.find_all('td')[2].text.strip()
            revenue = row.find_all('td')[6].text.strip()
            results = [impression, revenue]
            result_list.append(results)
        except Scraper_Exception:
            result_list.append(['login failure occured','login failure occured'])

        finally:
            return result_list

    def scrapeData_Darriens(self, browser):
        result_list = []
        soup = bsoup(browser.page_source, 'html.parser')
        try:
            row = soup.find_all('table')[0]
            impression = row.find_all('td')[2].text.strip()
            revenue = row.find_all('td')[5].text.strip()
            results = [impression, revenue]
            result_list.append(results)
        except Scraper_Exception:
            result_list.append(['login failure occured','login failure occured'])

        finally:
            return result_list

class LKQD(LKQD_Scraper, WebDriver_Exception):

    def __init__(self, cred):
        self.cred = cred

    def exe(self):
        yesterday = date.today() - timedelta(1)
        browser = webdriver.Firefox()
        wait = WebDriverWait(browser, 15)
        browser.get("https://ui.lkqd.com/login")
        try:
            userElement = wait.until(EC.visibility_of_element_located((By.ID, 'username')))
            userElement.send_keys(self.cred.pop('User'))
            passElement = browser.find_element_by_id("password")
            passElement.send_keys(self.cred.pop('Password'))
            browser.find_element_by_class_name("btn.btn-primary").click()
            time.sleep(10)
        except WebDriver_Exception:
            print(self.cred['Advertiser'] + "login failed")
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'form-control'))).click()
            # browser.find_element_by_class_name("form-control").click()
            time.sleep(1)
            browser.find_element_by_xpath("/html/body/div[2]/div[3]/ul/li[2]").click()
            time.sleep(.5)
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'run-report-button.btn.btn-success'))).click()
            # browser.find_element_by_class_name("run-report-button.btn.btn-success").click()

        except WebDriver_Exception:
            self.cred['Impression'] = 'Web Driver Crashed'
            self.cred['Revenue'] = 'Web Driver Crashed'
        time.sleep(3)
        if self.cred['Advertiser'] == 'Darriens':
            scraped_list = LKQD_Scraper().scrapeData_Darriens(browser)
        else:
            scraped_list = LKQD_Scraper().scrapeData(browser)
        self.cred['Impression'] = scraped_list[0][0]
        self.cred['Revenue'] = scraped_list[0][1]
        self.cred['Date'] = yesterday.strftime('%m%d%y')
        browser.quit()
        DB.Access_DB('external_partners.db').load(self.cred)

class Streamrail_Scraper(Scraper_Exception):

    def scrape(self, browser):
        result_list = []
        soup = bsoup(browser.page_source, 'html.parser')
        try:
            totals_row = soup.find_all('div', { "class": 'row sr-collection--summary-row no-horizontal-margin valign-wrapper blue-grey lighten-5'})[1]
            imp_row = totals_row.find_all('div')[3]
            impression_r = imp_row.find_all('span', {'class': 'sr-collection--summary-numeric'})
            impression = impression_r[0].text.strip()
            rev_row = totals_row.find_all('div')[5]
            revenue_r = rev_row.find_all('span', {'class': 'sr-collection--summary-numeric'})
            revenue = revenue_r[0].text.strip()
            results = [impression, revenue]
            result_list.append(results)
        except Scraper_Exception:
            result_list.append(['No Data returned','No Data returned'])

        finally:
            return result_list

class Streamrail(Streamrail_Scraper,WebDriver_Exception):

    def __init__(self, cred):
        self.cred = cred

    def exe(self):
        yesterday = date.today() - timedelta(1)
        browser = webdriver.Firefox()
        wait = WebDriverWait(browser, 15)
        browser.get("https://partners.streamrail.com")

        try:
            userElement = wait.until(EC.visibility_of_element_located((By.ID, 'ember730-input')))
            userElement.send_keys(self.cred.pop('User'))
            passElement = browser.find_element_by_id("ember751-input")
            passElement.send_keys(self.cred.pop('Password'))
            browser.find_element_by_class_name("btn.sr-primary-btn.waves-effect.waves-light.white-text.action-btn.right").click()
        except WebDriver_Exception:
            self.cred['Impression'] = 'Login error'
            self.cred['Revenue'] = 'Login error'

        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'ember-power-select-trigger.ember-basic-dropdown-trigger.ember-view'))).click()
            # browser.find_element_by_class_name("ember-power-select-trigger.ember-basic-dropdown-trigger.ember-view").click()
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR,'li.ember-power-select-option:nth-child(2)'))).click()
            # browser.find_element_by_css_selector('li.ember-power-select-option:nth-child(2)').click()
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'btn-toolbar-icon.sr-primary-btn.waves-light.waves-effect.btn.ember-view'))).click()
            # browser.find_element_by_class_name('btn-toolbar-icon.sr-primary-btn.waves-light.waves-effect.btn.ember-view').click()

        except WebDriver_Exception:
            self.cred['Impression'] = 'Web Driver Crashed'
            self.cred['Revenue'] = 'Web Driver Crashed'

        except TimeoutException:
            self.cred['Impression'] = "Error in UI"
            self.cred['Revenue'] = "Error in UI"
            self.cred['Date'] = yesterday.strftime('%m%d%y')

        time.sleep(4)
        scraped_list = Streamrail_Scraper().scrape(browser)
        try:
            self.cred['Impression'] = scraped_list[0][0]
            self.cred['Revenue'] = scraped_list[0][1]
            self.cred['Date'] = yesterday.strftime('%m%d%y')
        except IndexError:
            self.cred['Impression'] = "No data returned"
            self.cred['Revenue'] = "No data returned"
            self.cred['Date'] = yesterday.strftime('%m%d%y')
        browser.quit()
        DB.Access_DB('external_partners.db').load(self.cred)

class Verta_Scraper(Scraper_Exception):

    def scrape(self, browser):
        result_list = []
        soup = bsoup(browser.page_source, 'html.parser')
        try:
            rev_row = soup.find_all('div', {"id":'vmw-dashboard-revenue-1017-innerCt'})[0]
            revenue_box = rev_row.find_all('div')[3]
            revenue = revenue_box.find_all('span')[1].text.strip()
            result_list.append(revenue)
            impression_row = soup.find_all('div', {"id":'vmw-dashboard-impressions-1018-innerCt'})[0]
            impression_box = impression_row.find_all('div')[3]
            impression = impression_box.find_all('span')[1].text.strip()
            result_list.append(impression)

        except Scraper_Exception:
            result_list.append(['login failure occured','login failure occured'])

        finally:
            return result_list

class Verta(Verta_Scraper, WebDriver_Exception):

    def __init__(self, cred):
        self.cred = cred

    def exe(self):
        browser = webdriver.Firefox()
        wait = WebDriverWait(browser, 15)
        yesterday = date.today() - timedelta(1)
        browser.get("https://ssp.vertamedia.com")

        try:
            userElement = wait.until(EC.visibility_of_element_located((By.ID,'textfield-1020-inputEl')))
            userElement.send_keys(self.cred.pop('User'))
            time.sleep(3)
            wait.until(EC.visibility_of_element_located((By.ID,'button-1021-btnInnerEl'))).click()
            passElement = wait.until(EC.visibility_of_element_located((By.ID, 'textfield-1027-inputEl')))
            passElement.send_keys(self.cred.pop('Password'))
            time.sleep(2)
            wait.until(EC.visibility_of_element_located((By.ID,'button-1028'))).click()

        except TimeoutException:
            self.cred['Impression'] = "Login error"
            self.cred['Revenue'] = "Login error"
            self.cred['Date'] = yesterday.strftime('%m%d%y')

        time.sleep(13)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'x-form-field.x-form-radio.x-form-radio-default.x-form-cb.x-form-cb-default'))).click()
        time.sleep(3)
        scraped_list = Verta_Scraper().scrape(browser)
        self.cred['Impression'] = scraped_list[1]
        self.cred['Revenue'] = scraped_list[0]
        self.cred['Date'] = yesterday.strftime('%m%d%y')
        browser.quit()
        DB.Access_DB('external_partners.db').load(self.cred)
