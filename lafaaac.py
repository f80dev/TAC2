from tools import Tools

class LaFaaac(Tools):
    def __init__(self,domain="https://lafaaac-webapp.teachonmars.com/category/scenario-1569572663",fastMode=True,quality=1):
        super().__init__(
            speech_engine="fr-FR-Standard-A" if quality == 0 else "fr-FR-Wavenet-A"
        )
        self.fastMode = fastMode
        self.go(domain)

    def login(self, username, password, quick=False):
        self.clavier(username,"login")
        self.clavier(password,"password")
        self.click("login tom-primary md-button md-tom-theme md-ink-ripple",0)
        self.wait(2)

    def open_module(self,index=0):
        modules=self.findall("image",self.find("items ng-scope"))

        if len(modules)>0 and index<len(modules):
            self.click(modules[index])
            self.back()
