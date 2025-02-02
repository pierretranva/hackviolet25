# -*- coding: utf-8 -*-
"""
Created on Sat Feb  1 22:53:00 2025

@author: LEO
"""

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
    
    def contains_ignore_case(self, sub_string, text):
        """Check if a substring is contained in a text, ignoring the case."""
        return sub_string.lower() in text.lower()

    def determine_site(self):
        if self.contains_ignore_case("linkedin", self.job_url):
            return 0 # LinkedIn
        elif self.contains_ignore_case("indeed", self.job_url):
            return 1 # Indeed
        else:
            return -1
        # This is only if the LLM is dumb ash
        

    def start_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        #chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def scrape(self):
        self.start_driver()
        try:
            site_type = self.determine_site()
            if site_type == 0:
                # LinkedIn
                self.details = self.linkedIn_ws()
            elif site_type == 1:
                # Indeed
                self.details = self.indeed_ws()
            else:
                print("Site Not Supported. Exiting...")
        finally:
            self.driver.quit()
            
            

    def linkedIn_ws(self):
        driver = self.driver
        # Login to LinkedIn
        driver.get("https://www.linkedin.com/login")
        time.sleep(1)
        
        # Login fields
        email_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "password")
        
        # Enter login credentials
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
                self.details = job_details_text
                print("Extracted Job Details Content:")
                print(job_details_text)
            else:
                print("No <p> element with dir='ltr' found inside div.mt4.")
        else:
            print("No div.mt4 found in the document.")
            
        return job_details_text
    
    def indeed_ws(self):
        driver = self.driver
        driver.get(self.job_url)
        
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "jobDescriptionText"))
            )
            print("Found the job description (Indeed).")
        except TimeoutException:
            print("Timed out waiting for the job details container (Indeed).")
            
        time.sleep(2)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        job_details_text = ""
        desc_container = soup.find("div", {"id": "jobDescriptionText"})
        if desc_container:
            job_details_text = desc_container.get_text(strip=True)
            self.details = job_details_text
            print("Extracted Job Details Content (Indeed):")
        else:
            print("No job description container found (Indeed).")
            
        return job_details_text

if __name__ == "__main__":
    job_url = ("https://www.indeed.com/viewjob?jk=1461e53d8433ad3c&from=shareddesktop"
               "?alternateChannel=search&refId=Sd48MmY2YFTvaB19EbuEwg%3D%3D"
               "&trackingId=EFDjWksO6ZI7bETjJkmGKA%3D%3D")
    scraper = WebScrape(job_url)
    scraper.scrape()
    print(scraper.get_details())