from tools import *

domain="http://localhost:4200"

class User:

    def __init__(self,index=0,username="",password=""):
        self.tools=Tools()
        if self.start(index):
            if len(username)>0:
                self.login(username,password)

    def prompt(self,text:str,cmd:str="cmdYes"):
        self.tools.set_field("txtPrompt",text)
        self.tools.click(cmd)
        self.tools.wait(0.2)


    def start(self,index=0,waiting=3):
        self.tools.mobile(position=index)
        self.tools.browser.goto(domain)
        return self.tools.waitFor("cmdCreateEvent")


    def number_events_to_buy(self):
        rc= len(self.tools.browser.buttons(name="cmdBuy"))
        return rc

    def store(self):
        self.tools.go(domain+"/store")
        return self.number_events_to_buy()

    def buy(self,index=0):
        if self.store()>0:
            self.tools.click("cmdBuy",index)

    def close(self):
        self.tools.browser.close()


    def create_event(self,index):
        self.store()
        self.tools.click("cmdCreateEvent")
        self.tools.click("template",index=index)
        bc=self.tools.click("cmdCreateFictif")
        self.tools.wait(3)
        return bc


    def publish_event(self,index):
        return self.tools.click("cmdPublish", index=index)




    def login(self,username, password):

        self.tools.go(domain+"/login")
        self.tools.subtitle("L'utilisateur choisi une connexion par email")

        self.tools.click("cmdEmail")
        self.prompt(username)
        self.tools.wait(1)
        self.prompt(password)
        if self.tools.waitFor("cmdGoStore"):
            self.tools.subtitle("Après connexion il est redirigé vers la billeterie")
            return self.tools.click("cmdGoStore")

        return False



    def end(self):
        self.tools.browser.close()