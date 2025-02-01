import requests
from bs4 import BeautifulSoup

class webscrape:
    def __init__(self, jobUrl):
        self.__jobUrl = jobUrl
        self.__keywords = ""
        self.__siteType = -1

    def determineSite(self, jobUrl):
        #this is only if the llm is dumb ash
        return 0
    
