import re
import time 
import json
from loguru import logger
from selenium import webdriver
from imap_tools import MailBox, Q
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class Yandex:

    def __init__(self):
        # fireFoxOptions = webdriver.FirefoxOptions()
        # fireFoxOptions.set_headless()
        # self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
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

        self.driver.get("https://passport.yandex.com/registration/mail")
        time.sleep(10)
        self.type_element("#firstname",self.FIRST_NAME)
        self.type_element("#lastname",self.LAST_NAME)
        self.type_element("#login",self.USERNAME)
        self.type_element("#password",self.PASSWORD)
        self.type_element("#password_confirm",self.PASSWORD)
        self.click_element("span.link_has-no-phone")
        time.sleep(1)
        self.type_element("#hint_answer",self.ANSWER)

yandex_obj = Yandex()
yandex_obj.register()
time.sleep(10)