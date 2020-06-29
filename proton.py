import re
import sys
import time 
import json
import random
import string
import requests
from loguru import logger
from selenium import webdriver
from imap_tools import MailBox, Q
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

class ProtonMail:

    def __init__(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless()
        self.driver = webdriver.Firefox(firefox_options=fireFoxOptions)
        self.driver = webdriver.Firefox()
        self.FIRST_NAME_LIST='Aadi,Aarav,Aarnav,Aarush,Aayush,Abdul,Abeer,Abhimanyu,Abhiramnew,Aditya,Advaith,Advay,Advik,Agastya,Akshay,Amol,Anay,Anirudh,Anmol,Ansh,Arin,Arjun,Arnav,Aryan,Atharv,Avi,Ayaan,Ayush,Ayushman,Azaan,Azad,Brijesh,Bachittar,Bahadurjit,Bakhshi,Balendra,Balhaar,Baljiwan,Balvan,Balveer,Banjeet,Chaitanya,Chakradev,Chakradhar,Champak,Chanakya,Chandran,Chandresh,Charan,Chatresh,Chatura,Daksh,Darsh,Dev,Devansh,Dhruv,Dakshesh,Dalbir,Darpan,Ekansh,Ekalinga,Ekapad,Ekavir,Ekaraj,Ekbal,Farhan,Falan,Faqid,Faraj,Faras,Fitan,Fariq,Faris,Fiyaz,Frado,Gautam,Gagan,Gaurang,Girik,Girindra,Girish,Gopal,Gaurav,Gunbir,Guneet,Harsh,Harshil,Hredhaan,Hardik,Harish,Hritik,Hitesh,Hemang,Isaac,Ishaan,Imaran,Indrajit,Ikbal,Ishwar,Jainew,Jason,Jagdish,Jagat,Jatin,Jai,Jairaj,Jeet,Kabir,Kalpit,Karan,Kiaan,Krish,Krishna,Laksh,Lakshay,Lucky,Lakshit,Lohit,Laban,Manan,Mohammed,Madhav,Mitesh,Maanas,Manbir,Maanav,Manthan,Nachiket,Naksh,Nakul,Neel,Nakul,Naveen,Nihal,Nitesh,Om,Ojas,Omkaar,Onkar,Onveer,Orinder,Parth,Pranav,Praneel,Pranit,Pratyush,Qabil,Qadim,Qarin,Qasim,Rachit,Raghav,Ranbir,Ranveer,Rayaan,Rehaannew,Reyansh,Rishi,Rohan,Ronith,Rudranew,Rushil,Ryan,Sai,Saksham,Samaksh,Samar,Samarth,Samesh,Sarthak,Sathviknew,Shaurya,Shivansh,Siddharth,Tejas,Tanay,Tanish,Tarak,Teerth,Tanveer,Udant,Udarsh,Utkarsh,Umang,Upkaar,Vedant,Veer,Viaannew,Vihaan,Viraj,Vivaan,Wahab,Wazir,Warinder,Warjas,Wriddhish,Wridesh,Yash,Yug,Yatin,Yuvraj,Yagnesh,Yatan,Zayan,Zaid,Zayyan,Zashil,Zehaan'
        self.FIRST_NAME=self.FIRST_NAME_LIST.split(",")[random.randint(0,len(self.FIRST_NAME_LIST.split(","))-1)]
        self.LAST_NAME_LIST='Aambaliya,Abhangi,Ajani,Ajudia,Akbari,Akvaliya,Amin,Amipara,Amreliya,Andani,Antala,Asalaliya,Asodariya,Atkotiya,Babariya,Baldha,Bambharoliya,Barasiya,Barejiya,Barvadiya,Bhadani,Bhalara,Bhanderi,Bhayani,Bhesaniya,Bhingradiya,Bhudiya,Bhut,Bhuva,Bodar,Boghra,Borad,Borsadiya,Buha,Butani,Chabhadiya,Chhayani.,Chhodavadiya,Chikhaliya,Chimediya,Chohaliya,Chothani,Chovatiya,Dabasiya,Damasiya,Dangariya,Desai,Devani,Dhaduk,Dhameliya,Dhami,Dhanani,Dhankecha,Dholariya,Dhorajiya,Dobariya,Domadiya,Donga,Dudhagara,Dudhat,Dudhatra,Dungarani,Faldu,Gadhethariya,Gadhiya,Gajera,Gajipara,Gami,Gangani,Garsondiya,Gelani,Gevariya,Ghelani,Ghoniya,Ginoya,Gothadiya,Godhani,Golani,Gondaliya,Gorasiya,Halai,Hapaliya,Hapani,Harkhani,Harsoda,Hidad,Hirani,Hirapara,Jagani,Jangvadiya,Jasani,Jesani,Jetani,Jiyani,Jodhani,Jogani,Kabariya,Kabra,Katba,Kachhadiya,Kachhi,Kakadiya,Kalkani,Kalsariya,Kamani,Kanani,Kapadiya,Kapupara,Kapuriya,Karad,Karkar,Kasvala,Kathiriya,Kathrotiya,Kerai,Khakhariya,Khatra,Khetani,Khichadiya,Khunt,Kikani,Kodinariya,Koladiya,Korat,Kotadiya,Kothari,Kothiya,Koyani,Kumbhani,Kunjadiya,Kyada,Lakhani,Lila,Limbani,Limbasiya,Lukhi,Lunagariya,Madani,Madhapariya,Malaviya,Mandanka,Mangroliya,Mansara,Marakana,Mathukiya,Mavani,Mayani,Meghani,Mendpara,Mepani,Moliya,Monpara,Monpariya,Morad,Moradiya,Movaliya,Mulani,Mungra,Mungalpara,Nadiyadhara,Nagani,Nakrani,Nandaniya,Nariya,Nasit,Nonghanvadra,Padmani,Padariya,Padsala,Paghdar,Paladiya,Pambhar,Panchani,Paneliya,Pansara,Panseriya,Pansuriya,Parakhiya,Parsana,Patodiya,Pipaliya,Pipalva,Pirojiya,Pokar,Polra,Ponkiya,Poshiya,Rabadiya,Radadiya,Rafaliya,Raiyani,Rajani,Rakholiya,Ramani,Ramoliya,Rangani,Rank,Ranpariya,Ribadiya,Rokad,Rudani,Rupapara,Rupareliya,Sabalpara,Sabhaya,Sagpariya,Sakariya,Sakhiya,Sakhreliya,Sakhvada,Sangani,Sanghani,Sardhara,Sarkheliya,Satani,Satasiya,Satodiya,Savakiya,Savaliya,Seladiya,Senjaliya,Shankhavara,Shekhaliya,Shekhda,Shingala,Shiyani,Sidpara,Siroya,Sojitra,Sonani,Sorathiya,Sudani,Sutariya,Suvagiya,Tadhani,Talaviya,Tanti,Tarapara,Tejani,Thesiya,Thumar,Thumbar,Tilala,Timbadiya,Togadiya,Trada,Trapasiya,Umretiya,Undhad,Usadad,Usadadiya,Vachhani,Vadi,Vadodariya,Vagadiya,Vaghajiani,Vaghani,Vaghasiya,Vaishnav,Vanpariya,Varsani,Vasani,Vasoya,Viradiya,Virani,Visavaliya,Vora,Vekariya,Zadafiya,Zalavadiya.,Chuvadia.,Dholakiya,Navadiya,Savani,Patoliya,Pandadiya,Goyani,Jivani,Shyani,Maniya,Bharodiya,Viththani,Gothaliya,Pethani,Gundaliya,Bonde,Babiya,Pedhadiya,Bagadiya,Hingladiya,Bandhaniya,Hala,Memagra,Akoliya,Valani,Gediya,Mangukiya,Saspara,Roy,Jajadiya'
        self.LAST_NAME=self.LAST_NAME_LIST.split(",")[random.randint(0,len(self.LAST_NAME_LIST.split(","))-1)]

        self.USERNAME = self.FIRST_NAME+self.LAST_NAME+str(random.randint(2000,10022))+str(random.randint(2000,5000))
        self.PASSWORD = self.randomString()

        self.RECOVERY_EMAIL = "jaydeepxas-" + self.USERNAME + "@yahoo.com"
        self.OTP_EMAIL = "jaydeepxas-" + self.USERNAME +"@yahoo.com"

        self.IMAP_SERVER = "imap.mail.yahoo.com"
        self.IMAP_USER = "jaydeepgajera24@yahoo.com"
        self.IMAP_PASS = "ucfksptvdxdtuorv"
        self.IMAP_FOLDER = "Inbox"

    def randomString(self,stringLength=12):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for i in range(stringLength))+"@"

    def iframe_select(self,iframe):
        if iframe != "" :
            try :
                logger.debug("iframe selection .. " + iframe)
                WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, iframe)))
                iframe = self.driver.find_element_by_css_selector(iframe)
                self.driver.switch_to.frame(iframe)
                # self.driver.implicitly_wait(30)
            except:
                pass

    def type_element(self,css_selector,value):
        logger.debug("typing - " + css_selector + " ... " + value)
        try:
            user_element = self.driver.find_element_by_css_selector(css_selector)
            user_element.send_keys(value)
            return True
        except Exception as ex:
            self.driver.quit()
            logger.error("Error change proxy." + css_selector)
            sys.exit()
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
            self.driver.switch_to.default_content()
            self.iframe_select("iframe.top")
            user_element = self.driver.find_element_by_css_selector(css_selector)
            logger.error(user_element.text)
            return True
        except Exception as ex:
            logger.error(ex)
            return False

    def create_yahoo(self):
        cookies = {
            'A3': 'd=AQABBA6X814CEKH-o_p9ZcWoV0EGx-YaK3IFEgEBAQHo9F79XgAAAAAA_SMAAAcIDpfzXuYaK3I&S=AQAAAulj0DEWfi_9nk11JG9djT8',
            'B': '74aoqspff75oe&b=3&s=s8',
            'A1': 'd=AQABBA6X814CEKH-o_p9ZcWoV0EGx-YaK3IFEgEBAQHo9F79XgAAAAAA_SMAAAcIDpfzXuYaK3I&S=AQAAAulj0DEWfi_9nk11JG9djT8',
            'A1S': 'd=AQABBA6X814CEKH-o_p9ZcWoV0EGx-YaK3IFEgEBAQHo9F79XgAAAAAA_SMAAAcIDpfzXuYaK3I&S=AQAAAulj0DEWfi_9nk11JG9djT8&j=WORLD',
            'GUC': 'AQEBAQFe9Ohe_UIfigSc',
            'T': 'af=JnRzPTE1OTM0MjgwNDAmcHM9RGZ2dkhZdEFkM0prT2x5UDlZZVVhUS0t&d=bnMBeWFob28BZwFVWlNPMlVGRVpSUzRLUFVWWEtHNUFNTk1TVQFhYwFBREFOcTZZYQFhbAFqYXlkZWVwZ2FqZXJhMjQBc2MBZGVza3RvcF93ZWIBZnMBd0ZXY2c2MWUuY2hJAXp6AUloYy5lQkE3RQFhAVFBRQFsYXQBSWhjLmVC&sk=DAAso6kckRz2jj&ks=EAAufjvBDELbI4h1NdED9UGdA--~G&kt=EAAgqvciKBpMViu1j6abKe6JA--~I&ku=FAAt2wvWqmZBb_VPsl4AgZ_S48Vss4HPGvz6XL30wIPtvbELKyd_Ke7UTxy_Ti7LO8IrWWIWukpbTzo3xTFqwnypIvoWMIRjJhuITrGbVVPzZlu3V_2Bw1ZH9Fcf5BgzADdktjkcQ2gtCRpwOeLNvUf7UvsmmhrINkwpWpXOB7GoTk-~D',
            'F': 'd=YBW5o609vJZW0fZDzyrInb31WpQ7W3UtPMxX8cB59ZsdzlM-',
            'PH': 'fn=0a0awh4_ol64cp5nZavyjw--&d=VfeTL0Hxe.PPK8WUKIx35LgN&s=hn&l=en-IN&i=in',
            'Y': 'v=1&n=09qrbfpp8qk0k&l=62nivt76udpkmblbd12glb2h9f6wd4ufh062mka9/o&p=m2tvvin00000000&r=174&intl=in',
            'AO': 'u=1',
            'GUCS': 'ASYftjw9',
            'cmp': 't=1593428047&j=0',
        }
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0',
            'Accept': 'application/json',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://mail.yahoo.com/',
            'Content-Type': 'multipart/form-data; boundary=---------------------------2516573416922065971360057260',
            'Origin': 'https://mail.yahoo.com',
            'TE': 'Trailers',
        }
        params = (
            ('name', 'settings.addAccount'),
            ('hash', '8b47b5ad'),
            ('appId', 'YMailNorrin'),
            ('ymreqid', 'fea1d713-9932-f209-1cda-410006010800'),
            ('wssid', 'UQ/YfLr1FkS'),
        )
        data = '''
-----------------------------2516573416922065971360057260
Content-Disposition: form-data; name="batchJson"

{"requests":[{"id":"AddAccount","uri":"/ws/v3/mailboxes/@.id==VjN-Vl4A73XJVri0hkczb5ZiaxUcs2OtRXuG8df7rFaFXrhsr3oTDFzkaEHLn7sxixRXarLONpzfaINE8EDSMWvd0g/accounts","method":"POST","payload":{"account":{"type":"DEA","email":"jaydeepxas-'''+self.USERNAME+'''@yahoo.com"}},"requests":[{"id":"GetAccounts","uri":"/ws/v3/mailboxes/@.id==VjN-Vl4A73XJVri0hkczb5ZiaxUcs2OtRXuG8df7rFaFXrhsr3oTDFzkaEHLn7sxixRXarLONpzfaINE8EDSMWvd0g/accounts","method":"GET"}]}],"responseType":"json"}
-----------------------------2516573416922065971360057260--
        '''
        # data = '-----------------------------135714806322613728122410847995\\r\\nContent-Disposition: form-data; name="batchJson"\\r\\n\\r\\n{"requests":[{"id":"AddAccount","uri":"/ws/v3/mailboxes/@.id==VjN-Vl4A73XJVri0hkczb5ZiaxUcs2OtRXuG8df7rFaFXrhsr3oTDFzkaEHLn7sxixRXarLONpzfaINE8EDSMWvd0g/accounts","method":"POST","payload":{"account":{"type":"DEA","email":"jaydeepxas-'+self.USERNAME+'@yahoo.com"}},"requests":[{"id":"GetAccounts","uri":"/ws/v3/mailboxes/@.id==VjN-Vl4A73XJVri0hkczb5ZiaxUcs2OtRXuG8df7rFaFXrhsr3oTDFzkaEHLn7sxixRXarLONpzfaINE8EDSMWvd0g/accounts","method":"GET"}]}],"responseType":"json"}\\r\\n-----------------------------135714806322613728122410847995--\\r\\n'
        response = requests.post('https://mail.yahoo.com/ws/v3/batch', headers=headers, params=params, cookies=cookies, data=data)
        logger.info(response.text)

    def check_mail(self):
        time.sleep(10)
        logger.info("checking mail of " + self.OTP_EMAIL)
        link = ""
        mailbox = MailBox(self.IMAP_SERVER)
        mailbox.login(self.IMAP_USER, self.IMAP_PASS, initial_folder=self.IMAP_FOLDER)
        try : 
            for mail in mailbox.fetch(Q(all=True)) :
                if mail.to[0] == self.OTP_EMAIL :
                    content = mail.text
                    for code in content.split() :
                        if code.isdigit():
                            link = code
        except:
            pass

        if link == "" :
            logger.info("didn't receive mail or mail problem")
            return self.check_mail()

        return link


    def register(self):
        logger.debug("register requested .... ")
        # Signup Form
        self.driver.get("https://mail.protonmail.com/create/new?language=en")
        time.sleep(10)
        self.iframe_select("iframe.top")
        self.type_element("#username",self.USERNAME)
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.iframe_select("iframe.bottom")
        self.type_element("#notificationEmail",self.RECOVERY_EMAIL)
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.type_element("#password",self.PASSWORD)
        self.type_element("#passwordc",self.PASSWORD)
        self.type_element("#passwordc",Keys.ENTER)
        time.sleep(10)
        if self.check_error('div.error'):
            self.iframe_select("iframe.top")
            self.type_element("#username",str(22))
            self.type_element("#username",Keys.ENTER)
            time.sleep(1)
        else:
            self.create_yahoo()

        self.click_element(".humanVerification-block-email  .signup-radio-label-text")
        time.sleep(3)
        self.type_element("#emailVerification",self.OTP_EMAIL)
        self.type_element("#emailVerification",Keys.ENTER)
        code = self.check_mail()
        logger.debug(code)
        self.type_element("#codeValue",code)
        self.click_element("button.humanVerification-completeSetup-create")
        response = requests.get("http://domesticfather.com/proton.php?data="+self.USERNAME+","+self.PASSWORD+"&status=register")
        logger.info(response.text)

while True:
    protonmail_obj = ProtonMail()
    protonmail_obj.register()
    time.sleep(15)
    protonmail_obj.driver.quit()
