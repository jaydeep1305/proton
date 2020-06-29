import re
import time 
import json
from loguru import logger
from selenium import webdriver
from imap_tools import MailBox, Q
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class MailCom:

    def __init__(self):
        # fireFoxOptions = webdriver.FirefoxOptions()
        # fireFoxOptions.set_headless()
        # self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)

        # profile = webdriver.FirefoxProfile()
        # user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        # profile.set_preference("general.useragent.override", user_agent)
        # self.driver = webdriver.Firefox(firefox_profile=profile)
        self.driver = webdriver.Firefox()

        self.USERNAME = "jaydeep1461a444"
        self.PASSWORD = "xa745s1@sdaq"
        self.FIRST_NAME = "Jaydeep"
        self.LAST_NAME = "Patel"
        self.ANSWER = "jaydeep145"
        self.RECOVERY_EMAIL = self.USERNAME + "@keepjpg.com"
        self.OTP_EMAIL = self.USERNAME + "@keepjpg.com"
        self.IMAP_SERVER = "imap.zoho.com"
        self.IMAP_USER = "admin@keepjpg.com"
        self.IMAP_PASS = "memyself555"
        self.IMAP_FOLDER = "Inbox"
        self.BIRTH_MONTH = "05"
        self.BIRTH_DAY = "13"
        self.BIRTH_YEAR = "1993"

    def iframe_select(self,iframe):
        if iframe != "" :
            logger.debug("iframe selection .. " + iframe)
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, iframe)))
            iframe = self.driver.find_element_by_css_selector(iframe)
            self.driver.switch_to.frame(iframe)
            self.driver.implicitly_wait(30)

    def type_element(self,css_selector,value):
        logger.debug("typing - " + css_selector + " ... " + value)
        try:
            user_element = self.driver.find_element_by_css_selector(css_selector)
            user_element.send_keys(value)
            return True
        except Exception as ex:
            logger.error(ex)
            return False

    def click_element(self,css_selector):
        logger.debug("click - " + css_selector)
        try:
            user_element = self.driver.find_element_by_css_selector(css_selector)
            user_element.click()
            return True
        except Exception as ex:
            logger.error(ex)
            return False

    def check_error(self,css_selector):
        try:
            user_element = self.driver.find_element_by_css_selector(css_selector)
            logger.error(user_element.text)
            return False
        except Exception as ex:
            logger.error(ex)
            return True

    def check_mail(self):
        time.sleep(10)
        logger.info("checking mail of " + self.OTP_EMAIL)
        link = ""
        mailbox = MailBox(self.IMAP_SERVER)
        mailbox.login(self.IMAP_USER, self.IMAP_PASS, initial_folder=self.IMAP_FOLDER)
        mails = [msg for msg in mailbox.fetch(Q(text=self.OTP_EMAIL))]

        for mail in mails:
            if "Proton Verification Code" in mail.subject:
                content = mail.text
                for code in content.split() :
                    if code.isdigit():
                        link = code
                # link = re.search('<(.*)>',content).group(1)                

        if link == "" :
            logger.info("didn't receive mail or mail problem")
            return self.check_mail()

        return link


    def register(self):
        logger.debug("register requested .... ")
        # Signup Form

        self.driver.get("https://signup.mail.com/")
        time.sleep(20)
        self.type_element('[data-test="check-email-availability-email-input"]',self.USERNAME)
        self.click_element('[data-test="check-email-availability-check-button"]')
        self.click_element('[name="salutation"]')
        self.type_element('[data-test="first-name-input"]',self.FIRST_NAME)
        self.type_element('[data-test="last-name-input"]',self.LAST_NAME)

        select = Select(self.driver.find_element_by_css_selector('[data-test="country-input"]'))
        select.select_by_value('IN')

        self.type_element('[data-test="month"]',self.BIRTH_MONTH)
        self.type_element('[data-test="day"]',self.BIRTH_DAY)
        self.type_element('[data-test="year"]',self.BIRTH_YEAR)
        self.type_element('[data-test="choose-password-input"]',self.PASSWORD)
        self.type_element('[data-test="choose-password-confirm-input"]',self.PASSWORD)
        
        self.click_element('[name="mobile-phone-checkbox"]')
        self.click_element('[name="contact-email-checkbox"]')
        self.type_element('[data-test="contact-email-input"]',self.RECOVERY_EMAIL)

mailcom_obj = MailCom()
mailcom_obj.register()
time.sleep(10)