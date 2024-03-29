from bs4 import BeautifulSoup

import undetected_chromedriver as uc

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options


class Parser:

    def __init__(self, start_city, destination_city, date):
        self.driver = self.set_driver_settings()
        self.start_city = start_city
        self.destination_city = destination_city
        self.date = self.date_format(date)

    # enters data into a form
    def fill_form(self):
        driver = self.driver
        action = ActionChains(driver)

        chose_one_way = driver.find_element(By.ID, 'ctl00_c_CtWNW_ltOneway').click()
        input_start_city = driver.find_element(By.ID, 'ctl00_c_CtWNW_ddlFrom-suggest')
        input_start_city.send_keys(self.start_city)
        action.send_keys(Keys.ARROW_DOWN)
        action.send_keys(Keys.ENTER)
        action.perform()
        input_destination_city = driver.find_element(By.ID, 'ctl00_c_CtWNW_ddlTo-suggest')
        input_destination_city.send_keys(self.destination_city)
        action.send_keys(Keys.ARROW_DOWN)
        action.send_keys(Keys.ENTER)
        action.perform()
        input_day = driver.find_element(By.ID, 'txtDepartDate').click()

        # it needs to be improved so that you can switch to the right month and year
        day_pick = driver.find_element(By.ID, self.date).click()

        submit = driver.find_element(By.ID, 'ctl00_c_IBE_PB_FF').click()

    def get_html_content(self):
        url = 'https://fly2.emirates.com/CAB/IBE/SearchAvailability.aspx'
        form_url = 'https://www.emirates.com/sessionhandler.aspx?pageurl=/IBE.aspx&pub=/english&j=f&section=IBE'
        driver = self.driver

        driver.get(url)
        driver.implicitly_wait(10)
        accept_cookies = driver.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        driver.get(form_url)

        self.fill_form()

        WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.ID, 'ctl00_IBEHeader_NEW_EK_LOGO_AN')))

        return driver.page_source

    # by using selenium, bypasses site blocking
    @staticmethod
    def set_driver_settings():
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument('--disable-blink-features=AutomationControlled')
        return uc.Chrome(options=options)

    @staticmethod
    def date_format(date):
        day = date.split('-')[2]
        if day[0] == '0':
            day = day[1]
        month = int(date.split('-')[1]) - 1
        year = date.split('-')[0]
        new_date = 'day-{0}-{1}-{2}'.format(day, month, year)

        return new_date

    # gets the information you need from the page
    # it needs to add the ability to catch more exceptions
    @staticmethod
    def get_flights(page_source):
        soup = BeautifulSoup(page_source, 'html.parser')

        if soup.find("div", attrs={"class": "errorPanel error"}):
            print(soup.find("div", attrs={"class": "errorPanel error"}).text)
            return "error"

        soup_all_flights = soup.find("div", attrs={"class": "ts-ifl__body"})

        flights = []
        for soup_flight in soup_all_flights.find_all("div", attrs={"class": "ts-ifl-row"}):
            flight = dict()
            flight['flight_time'] = soup_flight.find("time", attrs={"class": "ts-fie__departure"}).text
            flight['flight_cost'] = soup_flight.find("div", attrs={"class": "ts-ifl-row__footer-price"}).text
            flights.append(flight)

        return flights
