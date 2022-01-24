from femis import FemisUser
from utils import words, digits, tirage, postal_address, build_date, random_email, random_name


class TutoFemis:
    users = list()

    def __init__(self,prod=False):
        self.f = FemisUser(prod=prod,fastMode=False)


    def quit(self):
        self.f.stop("Fin du tutoriel",subtitle="Réalisation F80 (f80.fr)",subdir="femis")
        self.f.quit()
        self.f.close()

    def scenario_create_user(self):
        self.f.capture(title="Création d'un contact externe")
        self.f.login("j.lecanu", "azerty")
        #self.users.append(self.f.create_contact("CONTACT", prenom="Paul", nom="Dudule", email="paul.dudule@gmail.com", phone=digits(8, "06")))
        self.f.stop()


    def scenario_build(self):
        self.f.capture(title="Création d'un étudiant")
        self.f.login("j.lecanu", "azerty",withTitle=False)
        #self.f.create_contact("STUDENT_FI",prenom="Paul",nom="Dudule",email="paul.dudule@gmail.com",complements={"PROMO":"ma promotion"})
        self.f.stop(title="Enregistrement du compte",subtitle="Après validation, le compte étudiant est créé et disponible dans le CRM")


    def scenario_inscription_sacre(self,firstname,lastname,email,password):
        self.f.capture(title="Inscription au parcours SACRe",subtitle="Connexion pour vérification de l'email")
        self.f.go(self.f.domain+"?apcafi=7")
        self.f.subtitle("La première étape consiste à s'inscrire avec son adresse mail")
        self.f.fill_form([firstname,lastname,email,password,password],first="fname",validate="btn btn-primary btn-block btn-lg js-btnSubmit")
        self.f.subtitle("La validation entraîne la vérification de l'email pour envoi d'un lien à ouvrir")
        self.f.click("btn btn-primary btn-close",0)
        self.f.stop(title="Parcours d'inscription")


    def scenario_fill_form(self,login:str,password:str):
        self.f.go(self.f.domain)
        #self.f.capture(title="Inscription SACRe",subtitle="Remplissage du formulaire")
        self.f.subtitle("Après avoir valider son compte en ouvrant le lien envoyé dans le mail de confirmation d'inscription,")
        self.f.subtitle("Le candidat peut se connecter pour commencer ou compléter son dossier")
        self.f.login(login, password,withTitle=False,withSubtitle=False)
        self.f.subtitle("Après connexion, il retrouve son dossier tel qu'il l'avait laissé")
        self.f.fill_sacre_form(2,"dudule","roger")
        self.f.stop(title="Fin du remplissage",subtitle="L'inscription prend fin après paiement et confirmation")





    def scenario_mailing(self,capture=False,_type="CONTACT"):
        self.f.subtitle("Pour les besoins du parcours, on créé d'autres contacts")
        self.f.login("h.hoareau", "Hh4271!!",withTitle=False)
        if capture:
            self.f.capture("mail_campagne", "Mailing à un ensemble de contacts","Constitution de la liste, rédaction du mail et expédition")

        #cts = self.f.create_contact_list("Ma Liste_" + words(5),
        #                            "Cette liste est utilisé pour la réalisation du toturial OASIS", index_type=8,
        #                            lst_contacts=[1,2,3,4],filter="dudule")
        mail_camp = self.f.create_mail_campagn(name="Ma campagne de mail_" + words(6),
                                          description="Campagne utilisée à des fins de test",
                                               expediteur="paul.dudule@gmail.com",exp_name="Paul Dudule")

        option=6
        if _type=="STUDENT_FI":option=4
        #option désigne le type d'individu visé par la campagne
        self.f.select_link_menu(option=option,subtitle="On sélectionne le type d'individue à cibler dans notre mailing")
        self.f.log("Attaché une liste de contact")

        # self.f.create_link("PropertyFields_CRM_LISTING",
        #                  [0,1,2,3], "Lié des contacts à la campagne",
        #                  "La liste de contacts est maintenant associé a la campagne",
        #                  filter="dudule")

        #self.click("btn btn-primary btn-sm btn-add_or_remove", 0)


        self.f.create_link("PropertyFields_"+_type,
                         [1], "Lié des contacts à la campagne",
                         "La liste de contacts est maintenant associé a la campagne",
                         filter="dudule")


        if self.f.create_mailing(mail_campagn=mail_camp,
                              type_mailing=1,
                              link_event=1,
                              subject="Mailing de test",title=words(5),subtitle=words(15),
                              mail_items=["ceci est le label",0,words(20),words(20)],
                              send=True
                              ):
            self.f.subtitle("La campagne est en cours d'envoi")

        #self.f.create_phone_campaign(name="Ma campagne de telephone", description=words(15), contacts=[0])

        self.f.wait(1)

        self.f.stop(title="Fin du tuto",subdir="femis")


    def create_stage(self,title="ouverture d'un stage",name="paul dudule"):
        self.f.login("h.hoareau", "Hh4271!!")
        #self.f.capture(title=title,subtitle="Décomposition de la procédure")

        if self.f.create_stage(
                name,["fonction de stagiaire","",""],
                societe="BAXTER",
                lieux=[postal_address("Address"),words(5),postal_address("CP"),postal_address("Ville"),"FRANCE"],
                representant=[1,random_name(),random_name(),words(1)],
                signataire=[1,random_name(),random_name(),words(3),digits(8,"06"),random_email()],
                sujet=["sujet du stage","Comment je me suis réconcillié, ma vie sexuelle / Arnaud Desch",words(6),1,random_name(),random_name(),digits(8,"06"),random_email(),words(3)],
                dates=["01/07/2020", "01/09/2020","no comment","pas de cas particuliers",4, 0, 1,100,"Travail exceptionnel le dimanche et certains jours fériés","Pas de modalité particulieres"]):
            self.f.go("#name=INTERNSHIP&type=LIST")
            self.f.show("hover detail",text="Dés validation le stage apparait dans la liste")

        self.f.stop(title="Procédure terminée",subtitle="Le stage peut ensuite être modifié ou simplement supprimé si besoin")
        return True




    def scenario2(self):
        self.f.capture("create_cours","Création d'un cours","Positionnement d'un cours, affectation d'une salle et choix des élèves")
        self.f.login("j.lecanu", "azerty")
        self.f.create_calendar("un si grand soleil","Formation pour tous")
        self.f.stop()
        return True



    def scenario_societe(self):
        self.f.login("h.hoareau", "Hh4271!!")
        self.f.capture("gestion_societe", "Gestion des sociétés",
                       "Création puis suppression d'une société")
        #self.f.find_societe(2,[[1,2],"coucou"])

        id=self.f.create_society(
            vals=["45456456","Dudule Corp","","4567-45678-7879-123",1,1,[3],0,0],
            address=["paul.dudule@gmail.com","","0144838356","12, rue Martel","","","75010","Paris",1,"Batiment C, code 2845"],
            comments=["numero du client","Nom de la société","maison mere s'il y en a une"],
            divers=["Société fictive créer pour la réalisation d'un tutoriel","Cette société ne doit pas être utiliser","Test","Test"])

        self.f.delete_societe(id)

        self.f.stop("Fin du tutoriel")


    def dedoublonnage(self,logins,seuil=100):
        self.f.login("h.hoareau", "Hh4271!!")
        for login in logins:
            self.f.go("https://femis.scolasis.com/#type=LIST&name=STUDENT_FI&operator=and&page=1&CODE="+login)
            if self.f.get_n_records()!=2:
                self.f.log("On doit avoir exactement 2 enregistrements pour réaliser une fusion")
            else:
                self.f.log("On demande la fusion de " + login)
                self.f.click("hover detail",0)
                self.f.openSideMenu(0, 5)
                self.f.fusion(seuil)
                self.f.wait(3)


    def dedoublonnage_societe(self,create_society=False):
        self.f.login("h.hoareau", "Hh4271!!")
        if create_society:
            id = self.f.create_society(
                vals=["45456456", "Dudule Corp", "", "4567-45678-7879-123", 1, 1, [3], 0, 0],
                address=["paul.dudule@gmail.com", "", "0144838356", "12, rue Martel", "", "", "75010", "Paris", 1,
                         "Batiment C, code 2845"],
                comments=["numero du client", "Nom de la société", "maison mere s'il y en a une"],
                divers=["Société fictive créer pour la réalisation d'un tutoriel",
                        "Cette société ne doit pas être utiliser", "Test", "Test"])
            id2 = self.f.create_society(
                vals=["45456456", "Dudule Corp", "", "4567-45678-7879-124", 1, 1, [3], 0, 0],
                address=["paul.dudule@gmail.com", "", "0144838356", "12, rue Martel", "", "", "75010", "Paris", 1,
                         "Batiment C, code 2845"],
                comments=["numero du client", "Nom de la société", "maison mere s'il y en a une"],
                divers=["Société fictive créer pour la réalisation d'un tutoriel",
                        "Cette société ne doit pas être utiliser", "Test", "Test"])

        self.f.go("#type=LIST&name=COMPANY")
        self.f.capture(title="Fusion de deux sociétés",subtitle="Identification des doublons par le nom et fusion des sociétés")
        self.f.set_filter("name","dudule",subtitle="Dans cet exemple on recherche des doublons par le nom")
        self.f.subtitle("Pour réaliser la fusion, on visualise le premier enregistrement")
        self.f.click("hover detail",0)
        self.f.openSideMenu(0,5,"Partant du principe qu'une fusion est possible on va étudier la différence entre les deux enregistrements")
        self.f.fusion()
        self.f.go("#type=LIST&name=COMPANY")
        self.f.subtitle("La liste ne comporte plus qu'un seul enregistrement")
        self.f.wait(1)
        return True

    def create_profil(self,type="STUDENT_FI",profils=[{"email":"herve.hoareau@f80.fr"}]):
        for p in profils:
            if isinstance(p,str):p=dict({"email":p})
            username=p["email"].split("@")[0]
            if not "firstname" in p:p["firstname"]=username.split(".")[0]
            if not "lastname" in p:
                if "." in username:
                    p["lastname"] = username.split(".")[1]
                else:
                    p["lastname"]="dudule"

            p["login"]=p["firstname"][0:1]+p["lastname"]
            c=None
            if type=="STUDENT_FI":
                c=self.f.create_contact("STUDENT_FI",[2,p["lastname"],p["firstname"],p["login"],"",True,
                                            p["email"],"",tirage(10000000,"06"),tirage(1000000,"01"),
                                            tirage(10000000,"06"),postal_address("address"),"",postal_address("CP"),postal_address("Ville"),1,
                                            build_date(delay=10000),1,1,
                                            tirage(2000000000),words(3),postal_address("all"),words(2),postal_address("all"),
                                            1,1,"",1,"",1,"The best",
                                            "Ceci est un étudiant fictif"])

            if type == "STUDENT_FC":
                c = self.f.create_contact("STUDENT_FC", [2, p["lastname"], p["firstname"], p["login"], "", True,
                                                         p["email"], "", tirage(10000000, "06"), tirage(1000000, "01"),
                                                         tirage(10000000, "06"), postal_address("address"), "",
                                                         postal_address("CP"), postal_address("Ville"), 1,
                                                         build_date(delay=10000), 1, 1,
                                                         1,"{{TAB}}",1,1,words(5),1,1,build_date(delay=30),build_date(),build_date(),10,words(10),"{{TAB}}",
                                                         1, 1, 1, 1, words(10),
                                                         "Ceci est un étudiant fictif"])

            if type=="CONTACT":
                c=self.users.append(self.f.create_contact("CONTACT",
                                                        [1, p["lastname"], p["lastname"], p["firstname"], "", "", "",
                                                         p["email"], digits(8, "01"),digits(8,"06"),
                                                         postal_address(prop="address"),"","",postal_address("cp"),postal_address("town"),1,
                                                         "","","","","","","","contact fictif"],first="GENDER"))

            if type=="PROF":
                c=self.f.create_contact("PROF", [
                    digits(20, "092"),
                    1,p["lastname"],p["lastname"],p["firstname"],"",build_date(100),words(2),0,digits(18),
                    postal_address("address"),"",postal_address("cp"),postal_address("ville"),0,digits(8,"01"),digits(8,"01"),digits(8,"06"),p["email"],"",postal_address("all"),
                    tirage(2),p["societe"],1,"OPV",0,1,0,"{{TAB}}","{{TAB}}",build_date(360),
                    "name:SOURCE=Hhoareau Automate fictif",0,0,words(3),"français"
                ],first="REFERENCE_NUMBER")

            if not c is None:
                self.users.append(c)
            else:
                self.f.log("Le type "+type+" est inconnu")




