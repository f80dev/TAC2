from selenium.webdriver.common.keys import Keys

from tools import Tools
from utils import extract, tirage, words, build_date, digits


class Flyview(Tools):
    def __init__(self,fastMode=True):
        super().__init__()
        self.start()
        self.fastMode=fastMode

    def start(self):
        self.size(1400,1000)
        self.domain = "https://www.flyview360.com/"
        self.go(self.domain)
        self.wait(2)
        self.click("js-cookies-close", 0)
        self.escape()
        self.metrics("home")
        self.show("activeLanguageDisplayer","La page d'acceuil est disponible en français ou en anglais")


    def buy_ticket(self):
        self.metrics("buy")
        self.title("Acheter des billets","Achat de 2 billets")
        self.go("https://tickets.flyview360.com/")
        if self.click("offre",1):
            zone=self.find("product odd",tirage(2))
            self.clavier("2",self.find("select",0,zone))
            self.click("btn tunnel-btn btn-next")
            self.click("day   available selected",tirage(5))
            self.metrics("buy_end")


    def buy_gift_card(self):
        self.metrics("buy_gift_card")
        self.go("https://tickets.flyview360.com/")
        self.click("consent",0)
        self.title("La carte cadeau")
        self.click(self.find("offre-tarif",4))
        zone = self.find("product odd", tirage(2))
        self.clavier("1", self.find("select", 0, zone))
        self.click("btn tunnel-btn btn-next")
        self.fill_infos()
        self.metrics("buy_gift_card_end")


    def fill_infos(self):
        self.fill_form(["hhoareau@gmail.com","hoareau","hervé",1," "," "],"zbSs3EtlXN")

    def back(self):
        self.browser.back()


























