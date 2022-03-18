from tools import Tools

class LaFaaac(Tools):
    def __init__(self,domain="",fastMode=True,quality=1,lang="fr-FR",showSubtitle=False):
        super().__init__(
            json_path="testandcapture-9fc576cad7c7.json",
            speech_engine="fr-FR-Standard-A" if quality == 0 else "fr-FR-Wavenet-A"
        )
        self.lang=lang
        self.showSubtitle=showSubtitle
        if lang=="en-US":self.speech_engine="en-US-Standard-A" if quality == 0 else "en-US-Wavenet-A"
        self.subdir="LaFaaac"
        self.fastMode = fastMode
        self.go(domain)

    def login(self, username, password, quick=False):
        self.go("https://lafaaac-webapp.teachonmars.com/login","La première connexion nécessite une identification")
        self.clavier(username,"login")
        self.clavier(password,"password")
        self.click("login tom-primary md-button md-tom-theme md-ink-ripple",0)
        return self.waitForURL("https://lafaaac-webapp.teachonmars.com/wall",20)

    def open_module(self,index=0):
        modules=self.findall("image",self.find("items ng-scope"))

        if len(modules)>0 and index<len(modules):
            self.click(modules[index])
            self.back()

    def show_store(self,swithOnStore=False):
        self.go("https://lafaaac-webapp.teachonmars.com/login")
        self.subtitle("L'application est téléchargeable sur les store")
        if swithOnStore:
            self.go("https://apps.apple.com/us/app/lafaaac/id1495631569","##pour iPhone",1)
            self.go("https://play.google.com/store/apps/details?id=com.lafaac.teachonmars.lafaac&gl=FR","##pour Android",1)
            self.subtitle("Egalement en version anglaise")
        else:
            self.show("storeLink ng-scope md-tom-theme ios","##pour iPhone")
            self.show("storeLink ng-scope md-tom-theme android","##pour Android")


    def intro(self):
        if not self.fastMode:
            self.insertCache("white",image=self.imageToBase64("./LaFaaac/LaFemisSolo.jpg"),delayInSec=2,size="50%",id_cache="test")
            self.wait(2)
            self.removeCache("test")

            self.insertCache("white",image=self.imageToBase64("./LaFaaac/Logo-LAFAAAC.png"),delayInSec=2,size="50%",id_cache="test")
            self.wait(2)
            self.removeCache("test")

            self.insertCache("white",image=self.imageToBase64("./LaFaaac/cnc.png"),delayInSec=2,size="50%",id_cache="test")
            self.wait(2)
            self.removeCache("test")

            self.insertCache("into_cache")
            self.subtitle("Lafaaac et La Fémis se sont associés avec le soutien du CNC",position="50vh",force=True)
            self.subtitle("pour développer un parcours de formation en mobile learning sur la dramaturgie sérielle",position="50vh",force=True)
            self.removeCache("into_cache")

            #self.title("",style="color:black;font-size:large;with:100%;text-align:center;",background="white")
            self.wait(1)


    def open_section(self,section_name,index,text):
        elt=self.find("title ng-binding",index)
        zone=self.find("caption",index-1)
        self.show(zone,section_name)
        self.click(elt)
        url=self.browser.url
        self.click("list ng-binding ng-scope",0,"Le module est disponible en plusieurs langues")
        self.waitForURL(url,disapear=True)
        text="##"+text.replace("|","|##")
        for txt in text.split("|"):
            self.wait(0.5)
            if len(txt)>2:
                self.subtitle(txt)
            self.scroll_down()

        self.wait(1)
        self.go("https://lafaaac-webapp.teachonmars.com/category/scenario-1569572663")


    def open_formation(self):
        self.go("https://lafaaac-webapp.teachonmars.com/catalog","Parmi les différentes offres de formation, vous trouverez la formation à l'atelier scénario")
        # elt=self.find("flickity-slider")
        # if elt:
        #     self.show(elt,text="Initiation à la Dramaturgie Sérielle")
        #     self.click(elt)
        self.go("https://lafaaac-webapp.teachonmars.com/training/0-scenario-bienvenue_2021_v1_ASF/activity/2_1")

        self.subtitle("Nos auteurs et formateurs sont des anciens élèves de La Fémis|$$Vincent Mariette|et Noémie de Lapparent")

        self.go("https://lafaaac-webapp.teachonmars.com/category/scenario-1569572663",
                "Ce parcours de formation est construit pour vous apporter les fondamentaux de la dramaturgie sérielle|Il est constitué de 5 chapitres d'un durée de 1h30 environ|Il est important de suivre l'ordre des chapitres")

        self.subtitle("Regardons plus en détail les différents modules")
        self.open_section("Les personnages",2,"Objectif Créer un personnage|et le connaitre dans les détails||")
        self.open_section("La bible",3,"Objectif Elaborer un document qui rassemble|tous les éléments clés de la série")
        self.open_section("L'épisode",4,"Objectif : Poser les promesses et|les jalons de la série à venir")
        self.open_section("La scène",5,"Objectif : chaque scène doit faire avancer l'histoire")
        self.open_section("Et une boite à outil pour le scénariste",6,"Maîtriser les pratiques clés pour réussir l'écriture de votre scénario")



    def detail_formation(self,url_home,title,url_first_page,text=""):
        self.go(url_home,title)
        self.go(url_first_page)
        for txt in text.split("|"):
            self.click("flickity-button flickity-prev-next-button next",0)
            self.subtitle(txt)
            self.wait(1)



    def show_settings(self):
        self.go("https://lafaaac-webapp.teachonmars.com/profile","Chaque utilisateur dispose d'un espace personnel")
        self.back()


    def logout(self):
        self.go("https://lafaaac-webapp.teachonmars.com/profile")
        self.click("md-icon-button action md-button ng-scope md-tom-theme md-ink-ripple")
        self.click("tom-primary md-button md-tom-theme md-ink-ripple")




        
