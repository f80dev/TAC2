from selenium.webdriver.common.keys import Keys

from tools import Tools
from utils import extract, tirage, words, build_date, digits


class LinkedinBot(Tools):
    def __init__(self,fastMode=True,proxy=""):
        super().__init__()
        self.start()
        self.fastMode=fastMode

    def start(self):
        self.size(1400,1000)
        self.domain = "https://www.linkedin.com/"
        self.go(self.domain)
        self.metrics("home")


    def open(self,person="hhoareau"):
        self.go(self.domain+"/in/"+person)



























