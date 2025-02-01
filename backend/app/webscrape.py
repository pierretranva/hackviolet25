from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time

class WebScrape:
    def __init__(self, job_url):
        self.job_url = job_url
        self.details = ""
        self.site_type = -1
        self.username = "couchcat1@gmail.com"
        self.password = "Thisisanalt123!"
        self.driver = None
    
    def get_details(self):
        return self.details

    def determine_site(self):
        # This is only if the LLM is dumb ash
        return 0

    def start_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        self.start_driver()
        try:
            self.details = self.linkedIn_ws()
        finally:
            self.driver.quit()
            

    def linkedIn_ws(self):
        driver = self.driver
        driver.get("https://www.linkedin.com/login")
        time.sleep(1)
        email_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        email_field.send_keys(self.username)
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)

        driver.get(self.job_url)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.mt4 p[dir='ltr']"))
            )
            print("Found the target <p> element with dir='ltr' inside div.mt4.")
        except TimeoutException:
            print("Timed out waiting for the job details container.")
        

        time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")


        div_mt4 = soup.find("div", class_="mt4")
        if div_mt4:
            p_ltr = div_mt4.find("p", attrs={"dir": "ltr"})
            if p_ltr:
                job_details_text = p_ltr.get_text(strip=True)
                print("Extracted Job Details Content:")
                print(job_details_text)
            else:
                print("No <p> element with dir='ltr' found inside div.mt4.")
        else:
            print("No div.mt4 found in the document.")

        return job_details_text

