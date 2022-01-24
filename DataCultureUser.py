from selenium.webdriver.common.keys import Keys

from tools import Tools


class DataCultureUser(Tools):
    def __init__(self,domain="http://localhost:4200",username="",password="",fastMode=True,quality=1):
        super().__init__(
            speech_engine="fr-FR-Standard-A" if quality==0 else "fr-FR-Wavenet-A"
        )
        self.fastMode=fastMode
        self.start(domain)

    def open_menu(self,item,text=""):
        self.clavier("{{ESC}}")
        menu=self.find(item)
        if menu is None or not menu.visible:
            self.click("cmdMenu")
            self.subtitle("Le menu latéral présente les principales commandes de l'outil")
            self.wait(2)

        self.click(item,text=text)


    def login(self,username,password,quick=False):
        if self.find("btnStart"):self.click("btnStart")
        if quick:
            self.go("http://localhost:4200/?login="+username+"&password="+password)
            self.wait(1)
        else:
            self.open_menu("cmdLogin","Data Culture est utilisable en mode connecté, pour accéder à plus de fonctionnalités")
            self.subtitle("Data Culture permet de se connecter avec son mail, mais également via Google")

            self.show("cmdEmail","Dans cette vidéo, nous allons utiliser l'authentification avec un mail")
            self.click("cmdEmail")

            self.wait(1)
            self.clavier(username,subtitle="L'utilisateur indique son adresse mail")
            self.wait(1)
            self.click("cmdYes")
            self.subtitle("Après validation, un code secret est immédiatement envoyé à l'utilisateur")

            self.clavier(password,elt="txtCode",subtitle="il saisie ce code")
            self.wait(1)
            self.click("cmdValider")
            self.wait(1.5)
            self.subtitle("L'utilisateur est immédiatement redirigé vers la fenêtre de recherche")
            self.subtitle("De nouvelles fonctionnalitées sont disponibles et les fiches étudiants présentent plus d'informations")

    def change_profil(self):
        self.open_menu("cmdEditPerms")
        self.subtitle("Plusieurs profils sont disponibles pour l'utilisateur, selon l'usage qu'il a de l'application")

        self.click("tabProfils", 3)
        self.show(self.find("cmdAskProfil",3),"Certains profils ne sont accessibles qu'après validation par la FEMIS")

        self.click("tabProfils", 4)
        elt=self.find("cmdAskProfil",4)
        self.show(elt, "D'autres profils sont accessibles immédiatement en ligne")
        return self.click(elt)




    def start(self,domain="http://localhost:4200/"):
        self.size(600,1000)
        self.domain = domain


    def search(self,text):
        self.subtitle("La fenêtre principale permet d'effectuer différentes recherches parmi les anciens étudiants de l'annuaire")
        self.subtitle("Ces recherches peuvent porter sur le nom, la promotion, les formations dispensées")
        self.wait(1)
        self.clavier(text+"{{ENTER}}","txtSearch","Illustrons ici une recherche par le nom de l'étudiant")
        self.wait(2)
        self.subtitle("Dès le début de la saisie, de premiers résultats apparaissent")



    def quit(self,title="Fin du tutoriel",subtitle=""):
        self.stop(title, subtitle=subtitle, subdir="data_culture")
        self.close()


    def explain_fiche(self,index=0):
        fiche=self.find("profils",index)
        if not fiche is None:
            self.wait(0.2)
            self.show(fiche,"De nombreuses informations sont accessibles depuis la fiche de chaque ancien étudiant",scale=1.5)
            self.show(self.find("lblDepartementCategorie", pere=fiche,onlyName=True), "La formation reçue durant sa scolarité")
            self.show(self.find("lblPromo", pere=fiche,onlyName=True), "Son année de sortie de l'école")
            self.show(self.find("cmdShareProfil", pere=fiche,onlyName=True), "Un accès direct à son profil détaillé")

            #self.show(self.find("lblCursus", pere=fiche), "Le type de cursus, formation professionnelle ou standard")

            if self.click("profils", index):
                self.wait(0.2)
                self.show(fiche,"Au dos de chaque profil se trouve l'ensemble des commandes permettant d'agir sur ce profil suivant les droits de l'utilisateurs")
                self.show(self.find("cmdContact", 0,pere=fiche,onlyName=True), "Envoyer un message")
                self.show(self.find("cmdOpenWork",0,pere=fiche,onlyName=True),"Voir l'ensemble des réalisations de cet étudiant")
                self.show(self.find("cmdLink", 0,pere=fiche,onlyName=True), "Accéder à la source d'où proviennent les informations du profil")
                self.show(self.find("cmdShareProfil",0, pere=fiche,onlyName=True), "Partager la fiche via ses réseaux sociaux")
                self.show(self.find("cmdEditProfil", 0,pere=fiche,onlyName=True), "Editer les informations de la fiche")
                self.show(self.find("cmdDelProfil", 0,pere=fiche,onlyName=True), "Ne plus être visible dans l'annuaire")
                return self.click(fiche)


    def show_realisation(self):
        fiche = self.find("cardAction", 1)
        self.click(self.find("cmdOpenWork",0,fiche))
        self.subtitle("Les expériences professionnelles de chaque profil sont disponibles à la consultation, si toutefois l'utilisateur dispose des droits requis")
        self.show("lstCategory","Pour faciliter la lecture, il est possible de filtrer les expériences par nature des oeuvres")
        self.show("lstJob","ou bien par poste occupé par le profil étudiant consulté")
        self.click("lstJob")
        self.clavier("{{ENTER}}")
        self.subtitle("Seules les expériences rendues publiques par le profil étudiant concerné apparaissent ici")
        self.wait(2)


    def explain_statistic(self):
        self.open_menu("cmdOpenStats","Data Culture propose un module statistique complet et simple d'utilisation")
        self.wait(2.5)
        self.click(self.find("btnStart", onlyId=True))
        self.wait(2.5)

        # tabs=self.findall("mat-tab-label-content",pere=self.find("tabStats"))
        self.subtitle("L'onglet Exports est dédié à l'exportation de l'ensemble des données")
        self.subtitle("L'onglet Documentation détail la signification de l'ensemble des champs exploitablent dans les rapports")

        lstReports=self.find("lstReports",onlyId=True)
        self.click(lstReports,"Différents rapports prédéfini sont accessibles directement dans l'outils")
        self.wait(1)
        self.clavier("{{ESC}}")

        self.click("lstFilter","Certain rapport peuvent être filtrer directement dans Data Culture")
        self.clavier("{{DOWN}}{{DOWN}}{{ENTER}}")
        self.wait(5.0)
        self.subtitle("Après la sélection du filtre, le rapport est immédiatement recalculé")

        self.subtitle("Plusieurs commandes permettent d'utiliser les statistiques en dehors de Data Culture")
        self.show(self.find("cmdOpen"),"Le rapport peut être ouvert dans un onglet dédié")
        self.show(self.find("cmdExport"),"Exporter sous Excel")
        self.show(self.find("cmdShare"),"Partager avec votre réseau")
        self.show(self.find("cmdRefresh"),"Ré-actualiser")
        self.show(self.find("cmdOpenSocialGraph"),"Il est également possible de faire une analyse du réseau relationnel des anciens")
        self.click("cmdBack")


    def explain_social_graph(self):
        self.open_menu("cmdOpenStats", "Data Culture propose un module statistique complet et simple d'utilisation")
        self.click(self.find("cmdOpenSocialGraph"),)
        self.wait(5)


    def explain_search(self,delay=3):
        self.subtitle("Data Culture propose un système de recherche des profils simple et rapide")
        self.clavier("ducournau","txtSearch","Il est possible de faire une recherche par nom")
        self.wait(delay)
        self.click("cmdCancel")

        self.clavier("julia","txtSearch","... par prénom")
        self.wait(delay)
        self.click("cmdCancel")

        self.clavier("1995", "txtSearch", "... par promotion",show=False)
        self.wait(delay)
        self.click("cmdCancel")

        self.clavier("réalisation", "txtSearch", "... par formation",show=False)
        self.wait(delay)
        self.click("cmdCancel")

        self.click("cmdExpertMode","Data Culture dispose également d'un mode de recherche plus sophistiqué")
        self.subtitle("Dans ce mode il est possible de combiner plusieurs critères comme la formation, le nom, le prénom")
        self.wait(2.0)
        self.click("cmdSimpleMode")


    def intro(self,generique=True):
        center="40vh"

        if generique:
            self.wait(1)
            self.insertCache(id_cache="intro")
            self.subtitle("Data Culture est un annuaire d'étudiants interactif",position=center)
            self.subtitle("Il donne une vision complète du parcours professionnel des anciens élèves de la FEMIS",position=center)
            self.subtitle("Il permet d'effectuer des recherches multi-critères sur l'ensemble des profils",position=center)
            self.subtitle("de consulter la filmographie de chaque profil étudiant",position=center)
            self.subtitle("d'obtenir des données statistiques anonymisées sur les parcours professionnels des anciens étudiants",position=center)
            self.removeCache(id_cache="intro")


    def first_screen(self,comment=True):
        self.go(self.domain)
        self.click(self.find("btnStart",onlyId=True))
        if comment:
            self.subtitle("Dès l'ouverture de l'application, le visiteur accède au catalogue des profils étudiants")
            self.show(self.find("profils",1),text="Chaque profil est présenté sous la forme d'une fiche individuelle")



    def open_panel(self,panel_name,texts:list,close=True):
        panel = self.find(panel_name,onlyName=True)
        if panel:
            self.click(panel)
            for text in texts:
                self.subtitle(text)
            if close: self.click(self.find("mat-expansion-panel-header",pere=panel))
            return self.find("mat-expansion-panel-header",pere=panel)
        return None


    def explain_edit_form(self):
        self.subtitle("Les informations sont regroupées par section")


        self.open_panel("pnlAdmin",["L'ensemble des informations personnelles du profil peuvent être mises à jour directement dans l'outil"])
        self.open_panel("pnlSocial",[
            "Chaque étudiant peut renseigner les principaux réseaux sociaux qu'il utilise",
            "Ces informations peuvent également être transmises lors d'une mise en relation avec d'autres profils"
        ])

        self.open_panel("pnlTutorat",[
            "Chaque étudiant peut se déclarer prêt à devenir le tuteur d'un autre étudiant","Tuteur signifie un contact privilégié avec l'étudiant tutoré"
        ])

        pnlExperience=self.open_panel("pnlExperience",[
            "Nous retrouvons ici l'ensemble des postes occupés par le profil sur différents films référencés dans Data Culture Pro",
            "Ces expériences peuvent avoir été saisies par le profil ou automatiquement récupérées via les principaux annuaires cinématographiques partenaires",
        ],close=False)

        self.show(self.find("cmdVisibilityOn", 0,pere=pnlExperience,onlyName=True),"Le profil peut contrôler la visibilité publique de chacune de ses expériences")
        self.show(self.find("cmdEdit", 0,pere=pnlExperience,onlyName=True),"il peut la modifier")
        self.show(self.find("cmdDeleteExperience", 0,pere=pnlExperience, onlyName=True), "enfin il peut la supprimer de Data Culture ")
        self.show(self.find("cmdAddExperience"),"Permet d'ajouter des expériences nons identifiées par le système")
        self.click(pnlExperience)

        self.open_panel("pnlAwards",[
            "L'ensemble des récompenses reçues est également disponible"
        ])

        self.wait(1)



    def edit_profil(self,index=0):
        if self.click("profils",index):
            self.click(self.find("cmdEditProfil",index),text="Le propriétaire de la fiche peut éditer les informations qu'elle contient")
            self.explain_edit_form()

        self.click("cmdClear",text="L'ensemble des expériences ajoutées automatiquement peut être effacée")
        self.wait(2)

        self.click("cmdAnalyse",text="Puis rechercher à nouveau par le système sur les principaux annuaires")
        self.wait(12)
        self.show("cmdAdd","Evidemment l'étudiant peut introduire manuellement autant d'expériences qu'il le souhaite")
        self.subtitle("La procédure commence par désigner le film concerné par l'expérience à ajouter")


    def add_experience(self,title="Comment je me suis disputé"):
        if self.waitForURL("/edit"):
            self.click("cmdAdd")

        if self.waitForURL("/addpow"):
            self.subtitle("Il est possible d'ajouter des films au référentiel de l'application")
            self.clavier(title,self.find("txtTitle"))
            self.wait(3)
            self.subtitle("Afin de limiter les doublons, le système propose la liste des films déjà référencés correpondant au nouveau titre")

            if len(self.findall("films"))>0:
                self.click(self.find("films",0))
            else:
                self.subtitle("Si le film n'est pas présent, l'utilisateur peut l'ajouter")
                self.click("cmdAddPow")
                self.subtitle("Pour ajouter un film, certaines informations sont demandées")
                self.clavier("bla bla bla bla bla ....",self.find("txtSynopsis"))
                self.clavier("2018",self.find("txtYear"))
                self.subtitle("Le synopsis et l'année de sortie sont obligatoires, les autres sont optionnelles")
                self.click("cmdSave")
                self.subtitle("Le film ajouté, il faut maintenant décrire l'expérience professionnelle vécue")

            self.subtitle("Le poste occupé parmi la liste des métiers disponibles est l'information principale et obligatoire")
            self.click("cmdAddExperience")
            self.subtitle("La nouvelle expérience vient automatiquement s'ajouter aux autres")

            idx=len(self.findall("cmdDeleteExperience"))-1
            self.click(self.find("cmdDeleteExperience",idx),text="Les expériences ajoutées manuellement peuvent être totalement supprimées du système")
            self.click("cmdYes")
            self.go(self.domain)



    def add_film(self):
        self.subtitle("Data Culture utilise un référentiel de films")
        self.open_menu("cmdAddMovie","Le gestionnaire du catalogue peut ajouter ou supprimer des films du référentiel")
        self.go(self.domain)

















