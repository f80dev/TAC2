from selenium.webdriver.common.keys import Keys

from tools import Tools
from utils import extract, tirage, words, build_date, digits


class FemisUser(Tools):
    def __init__(self,username="",password="",fastMode=True,prod=False):
        super().__init__()
        self.start(prod)
        self.fastMode=fastMode
        self.login(username, password)

    def start(self,prod=False):
        self.size(1400,1000)

        if prod:
            self.domain ="https://femis.scolasis.com/"
        else:
            self.domain = "https://testfemis.scolasis.com/"

        self.go(self.domain)


    def removeAlert(self):
        zone=self.find("alert alert-danger alert-dismissible navbar-fixed-bottom")
        if not zone is None:
            self.click(self.find("button",0,zone))
            return True
        else:
            return False


    def login(self,username,password,withTitle=True,withSubtitle=True):
        if len(username)>0 and len(password)>0:
            if self.find("NotificationMiniCenter",onlyId=True) is None:
                if withTitle:self.title("Connexion à OASIS", "usage du login et du mot de passe")
                if withSubtitle:self.subtitle("Pour se connecter, on utilise l'identifiant et le mot de passe fourni par l'administrateur à la création du compte")
                self.fill_form([username,password])
                self.show("themeMainColor pull-right flipLink","En cas d'oublie, on peut toujours se faire renvoyer son mot de passe")
                rc=self.click("btn btn-primary btn-block btn-lg",0)
                if withSubtitle:
                    self.subtitle("L'utilisateur est automatiquement reconnecté sur sa dernière page consultée")
                else:
                    self.wait(1)
                self.removeAlert()
                return rc
            else:
                self.log("Connexion déjà établie")

        return False

    def create_campagn(self,name,description="",sender=""):
        self.click("MenuCRM_CAMPAIGN_MAIL")
        self.click("toolbar-link highlight")
        self.set_field("NAME",name,0)
        self.set_field("DESCRIPTION", description,0)
        self.select("form-control col-2",sender)
        self.click("btn btn-lg btn-danger floating_toolbar",0)

    def quit(self):
        self.click("nav navbar-nav navbar-left navbar-with-dropdown",1)
        self.click("icon-off")

    def close(self):
        self.browser.close()


    def select_contact(self,type,login):
        self.go("#type=LIST&name="+type+"&CODE="+login)
        self.click("icon-eye",0)

    def select_contact(self,name):
        self.click("MenuSTUDENT_FI")
        self.set_field("LNAME",name,0)
        self.click("action_button btn-group wide")
        self.click("icon-eye",0)


    def create_profil(self, vals):
        self.go("#type=INSERT&name=PROFILE")
        self.fill_form(values=vals,first="CODE")
        return vals[0]


    def create_bloc(self, vals,desc):
        self.go("#type=INSERT&name=MODULE")
        self.fill_form(values=vals,first="CODE")
        self.click("MODULEdescription")
        self.browser.send_keys(Keys.TAB)
        self.fill_form(values=desc, first="CODE")
        self.click("CODE_PROFILEPROFILEInput")
        self.select_in_list([3,2])
        self.find("PropertyFields_PROFILE").elements(tag_name="button")[1].click()
        return vals[0]



    def create_stage(self, student,documents,societe,lieux,representant,signataire,sujet,dates):
        self.go("#type=INSERT&name=INTERNSHIP")
        self.subtitle("La première étape de création d'un stage commence par sélectionner l'étudiant concerné par le stage")
        self.click(self.pere(self.find("STUDENT", 0)))
        self.select_in_list(student,student, multi=False)
        self.fill_form(documents,first="POSITION")
        self.click("ATabLocation")

        self.subtitle("Dans l'onglet suivant on précise la société proposant le stage, le lieu et les représentants")
        self.click(self.pere(self.find("COMPANY",0)))
        self.select_in_list(societe,societe,multi=False)
        self.fill_form(lieux,first="INTERNSHIP_BUSINESS_ADDRESS-1-ADDRESS")
        self.fill_form(representant, first="CIE_REP_GENDER")
        self.fill_form(signataire,first="CIE_SIGNATORY_GENDER")
        self.click("ATabSubject")

        self.subtitle("Ici, on va préciser le sujet du stage et donner des informations sur le tuteur")
        self.fill_form(sujet,first="SUBJECT")
        self.click("ATabDates")
        self.subtitle("Cette zone va permettre de préciser les périodes de stage et le volume horaire")
        zone_dates = self.find("form-nested form-grid form-edit ui-sortable", 0)
        if not zone_dates is None:
            self.show(zone_dates, "Cette zone va permettre de saisir toutes les périodes du stage")
        self.fill_form(dates,first="{{TAB}}")

        self.click("btn btn-lg btn-danger floating_toolbar",0,text="La saisie terminée, on valide le stage")
        return True




    def create_society(self,vals:list,comments=list(),address=list(),divers=list()):
        """

        :param vals: liste suivante : numéro_client, nom, maison mere (list), siret, a_prospecter (liste), categorie
        :return:
        """
        self.go("#type=LIST&name=COMPANY")
        self.title("Création d'une société")
        self.wait(0.2)
        self.subtitle("La création se fait depuis l'onglet société, à partir de la liste de l'ensemble des sociétés par l'usage du bouton NOUVEAU")

        self.go("#type=INSERT&name=COMPANY")
        self.subtitle("Le formulaire se divise en plusieurs sections. Certains champs sont obligatoires (marqués d'une étoile rouge), d'autres non")
        self.fill_form(vals,first="CUSTOMER_CODE",comments=comments)
        self.fill_form(address,first="MAIL")
        self.fill_form(divers, first="INFO_SOURCE")
        self.click("btn btn-lg btn-danger floating_toolbar",0)
        self.show(self.find("hover detail",0),"La société est immédiatement visible dans la liste")
        self.subtitle("Les sociétés sont utiles pour saisir les taxes d'apprentissage, affecter les stages, gérer les contacts extérieurs")
        return extract(self.browser.url,"code=","&")




    def create_contact(self, type="STUDENT_FI",props=list(),complements=dict(),password="",first="GENDER"):
        self.go("#type=INSERT&name="+type)
        self.subtitle("Les champs obligatoires sont marqués d'une étoile rouge")
        self.subtitle("L'utilisateur peut choisir le mot de passe de l'étudiant ou demandé au système de le générer aléatoirement")
        if type=="STUDENT_FI":
            if len(password)==0:
                self.click("generatePassword btn btn-primary")
            else:
                self.clavier(password,"PASSWORD")
        else:
            self.browser.send_keys(Keys.TAB)

        self.fill_form(props,first=first)

        # if len(birthdate)>0:
        #     self.scroll_down()
        #     zone=self.pere(self.find("label","DATE DE NAISSANCE"))
        #     self.fill_form([birthdate,country,nationality],first=self.find("input",0,zone))

        for k in complements.keys():
            self.clavier(complements[k],k)

        #self.fill_form(["",nom,"",prenom,"","","",email,"",phone,address],first="GENDER",validate="btn btn-lg btn-danger floating_toolbar")
        self.subtitle("La validation entraine la création du contact",position="top")
        self.click("btn btn-lg btn-danger floating_toolbar",0)
        self.waitForURL("&code=")
        rc= extract(self.browser.url,"&code=","&")
        return rc

    def delete_contact(self, type,login):
        self.title("Suppression d'un contact")
        self.go("#type=LIST&name=" + type + "&CODE=" + login)
        self.click("btn-delete tip", 0,text="L'usage de la poubelle permet la suppression directement depuis la liste")
        self.click("btn btn-danger btn-delete",0)

    def delete_contacts(self,type="CONTACT",name="dudule",prenom=""):
        url="https://femis.scolasis.com/#type=LIST&name="+type+"&operator=and&page=1&LNAME="+name
        if len(prenom)>0:url=url+"&FNAME="+prenom
        self.go(url)
        zone_list=self.find("table table-striped table-hover",0)
        while True:
            elt=self.find("icon-trashcan",0,zone_list)
            if elt is None:break
            self.click(self.pere(elt))
            self.click("btn btn-danger btn-delete",0)
            self.wait(3)


    def select_link_menu(self,id_menu="assoc_tab nav nav-tabs",option=0,subtitle=""):
        zone=self.find(id_menu,0)
        if len(subtitle)>0:self.show(zone,subtitle)
        self.click(self.find("li",option,pere=zone))


    def create_contact_list(self,name,description="",index_type=8,lst_contacts:list=[1],filter=""):
        """
        :param name:
        :param description:
        :param index_type:
        :return:
        """
        self.title("Création d'une liste de contacts")
        self.go("#type=INSERT&name=CRM_LISTING")
        self.subtitle("Chaque liste de contact doit avoir un nom et une éventuelle description")
        self.fill_form([name,description],first="NAME",validate="ENTER")

        zone=self.find("assoc_tab nav nav-tabs",0)

        self.show(zone,"Cette zone contient l'ensemble des types de contacts pouvant être insérés. On peut également ajouter les contacts d'autres campagnes")

        option=self.find("set_assoc_tab",index_type,zone)
        if self.click(option,text="On choisit un type de contact à insérer dans la liste proposée"):
            self.create_link(id_zone="PropertyFields_CONTACT",
                             lst=lst_contacts,
                             filter=filter,
                             text="Sélectionner des contacts à inclure dans la liste",
                             show_result="L'ensemble des contacts inclus dans la liste est affiché immédiatement",
                             description_zone="Cette zone va permettre de sélectionner les contacts à introduire dans la liste à construire")
            self.subtitle("La liste de contact va pouvoir être utilisée pour le mailing")
            return name
        else:
            return None



    def create_mail_campagn(self, name, description,expediteur="",exp_name=""):
        self.go("#type=INSERT&name=CRM_CAMPAIGN_MAIL")
        self.title("Création d'une campagne de mail","Associé un mail type avec un ensemble de contacts")
        self.fill_form([name, description,1,expediteur,exp_name], first="NAME",validate="btn btn-lg btn-danger floating_toolbar")
        return name


    def create_calendar(self,item,title,comment=""):
        self.go("#codepage=CALENDAR")
        filter=self.find("input",0,self.find("CalInsertdataTable_courses_filter"))
        self.show(filter,"La liste des cours étant importante, il est préférable d'utiliser le filtre pour retrouver rapidement le cours à planifier")
        self.clavier(item,filter)
        elt=self.find("div",0,self.find("CalInsertdataTable_courses"))
        self.show(elt,"On va sélectionner le cours, présent dans la liste après application du filtre")
        self.subtitle("On sélectionne la semaine ou l'on souhaite positionner le cours")
        for i in range(2,int(tirage(7))):
            self.click("glyphicon glyphicon-chevron-right",0)

        self.subtitle("Puis on le fait glisser sur le jour souhaité")
        elt.drag_and_drop_by(400, 0)

        elt=self.find("fc-time-grid-event fc-v-event fc-event fc-start fc-end fc-draggable fc-resizable",0)
        self.click(elt,"On peut maintenant lui affecter des élèves, ou un cours")
        self.fill_form([title,comment],first="TITLE_FR")
        self.click("btn btn-default btn-sm close_popup",0)



    def create_link(self, id_zone, lst, text,show_result="",description_zone="",filter=""):
        """
        Permet de créer des liens avec les entités référentes
        :param id_zone:
        :param lst:
        :param text:
        :return:
        """
        self.show(id_zone,description_zone)
        zone = self.find(id_zone, 0)
        button = self.find("button", 0, zone)
        self.click(button, text)
        self.select_in_list(lst,filter=filter)
        valide=self.find("button", 1, zone)
        self.click(valide)
        if len(show_result)>0:
            self.show("table table-striped table-hover",show_result)


    def create_mailing(self, mail_campagn, type_mailing, link_event,subject,mail_items:list,title="",subtitle="",send=False,export=False):
        self.title("Finalisation du mailing","Selection du contenu & expédition")
        self.go("#type=INSERT&name=MAILING")
        self.fill_form([mail_campagn,type_mailing,link_event],first="CODE_CRM_CAMPAIGN",comments=[
            "On commence par désigner la campagne à utiliser pour le mailing",
            "Le type de mail est utilisé avec la gestion des consentements des destinataires",
            "Il est possible d'associer ou pas le mailing à un événement"
        ])
        self.click(self.find("a",1,self.find("tab-form nav nav-tabs",0)))
        self.fill_form([subject, title, subtitle], first="SUBJECT")

        self.write_mail(mail_items)

        self.click("btn btn-lg btn-danger floating_toolbar",0)

        self.openSideMenu(pave=2, option=0)
        zone_modal=self.find("ShowOptionsForm")
        self.click(self.find("btn btn-lg btn-danger",pere=zone_modal) , 0,"On génére le corps du mail")
        self.show("form-group form_field-horizontal clearfix odd",text="L'utilisateur peut visualiser le mail qui sera reçu avant de déclencher l'envoi")

        if send:
            self.log("Envoi du mail")
            self.openSideMenu(pave=2,option=1)
            self.click("btn btn-lg btn-danger",0,"On déclenche l'envoi")
        if export:
            self.openSideMenu(pave=1, option=0)

        return True


    def create_phone_campaign(self, name, description, contacts):
        self.title("Fabrication d'une campagne d'appels téléphonique")
        self.go("#type=INSERT&name=CRM_CAMPAIGN_PHONE")
        self.fill_form([name,description],first="NAME",validate="ENTER")
        self.create_link("PropertyFields_CRM_LISTING",contacts,"On ajoute les contacts à joindre par téléphone","La liste de contacts sont maintenant associé à la campagne")
        self.openSideMenu(pave=2,option=0)

    def openSideMenu(self, pave, option,subtitle=""):
        zone = self.find("side_content-links", pave, self.find("SideContent"))
        self.click(self.find("a", option, zone),text=subtitle)

    def fill_sacre_form(self,delayInSecBetweenScreen,nom,prenom,address="12 rue martel",ville="paris"):
        self.go("#codepage=CDT___INSTRUCTIONS_FI")
        self.wait(delayInSecBetweenScreen)
        self.go("#codepage=CDT___CIVILITY_FI",subtitle="Le candidat doit renseigner l'ensemble des paramètres liés à la civilité")
        self.fill_form([0,nom,prenom,"",build_date(30),words(3),1,1,digits(10)],first="GENDER")

        self.scroll_down()
        self.click(self.pere(self.find("IDPHOTO")))
        self.wait(1)
        #TODO: ne fonctionne pas
        self.browser.send_keys("text{ENTER}")


        self.scroll_down()
        self.fill_form([address,"",digits(5),ville,10],first="ADDRESS")
        self.wait(delayInSecBetweenScreen)
        self.click("btn btn-lg btn-danger floating_toolbar", 0)

        self.wait(delayInSecBetweenScreen/2)

        self.go("#codepage=CDT___WISHES_FI",subtitle="Il précise ensuite quelles sont les aides dont il dispose")
        self.wait(delayInSecBetweenScreen)
        self.go("#codepage=CDT___STUDIES_FI",subtitle="Quelles sont les études poursuivi jusqu'à maintenant")
        self.wait(delayInSecBetweenScreen)
        self.go("#codepage=CDT___ACTIVITIES_FI",subtitle="Puis ses productions et publications")
        self.wait(delayInSecBetweenScreen)
        self.go("#codepage=CDT___FOLDER_FI",subtitle="Enfin il transfmet à l'école les différents documents nécéssaires à la validation du dossier")
        self.wait(delayInSecBetweenScreen)




    def write_mail(self, mail_items):
        """
        Rédaction d'un email
        :param mail_items:
        :return:
        """
        cmdCreateMail = self.find("icon-plus-sign more", 0)
        self.click(cmdCreateMail, text="On créé un premier élément dans le corps de l'email")
        self.wait(0.5)
        self.clavier(Keys.TAB)
        self.subtitle("Puis on remplie les différentes zones")
        self.fill_form(mail_items)
        return True

    def delete_societe(self, id):
        self.go("#num=1&type=LIST&name=COMPANY")
        self.title("suppression d'une societe")
        self.go("#code="+str(id)+"&num=1&type=DETAIL&name=COMPANY")
        self.openSideMenu(0,1,subtitle="Cette option permet de supprimer la société ouverte")
        self.click("btn btn-danger btn-delete",0)
        self.subtitle("La société est immédiatement retirée de la liste")

    def find_societe(self,index_filter=-1,vals=list()):
        self.go("#num=1&type=LIST&name=COMPANY")
        if index_filter>=0:
            zone=self.add_filter(index_filter)
        self.fill_form(vals,first=self.find("MoreFiltersButton"))

    def add_filter(self,filter):
        zone=self.find("MoreFiltersButton")
        self.click(zone)
        rc=self.click(self.find("a",filter,self.pere(zone)))
        return zone


    def set_filter(self, field:str, value,subtitle=""):
        """
        Force le filtre
        :param field:  nom du champs à filtre
        :param value: valeur filtrée
        :param subtitle:
        :return:
        """
        zone = self.find("SideContent")
        self.clavier(value,elt=self.find(field.upper(),0,zone),subtitle=subtitle)
        return self.click(self.find("action_button btn-group wide",0,zone))


    def get_n_records(self):
        if "#type=LIST" in self.browser.url:
            elt=self.find("themeMainColor")
            if elt is None:
                self.log("Impossible de trouver le nombre d'enregistrement")
                return None
            return int(elt.inner_text)
        else:
            self.log("Il faut être en présence de liste pour retourner le nombre d'enregistrement")
            return None



    def fusion(self,seuil=90):
        """
        Réalise la fusion de deux enregistrement
        """
        self.wait(1)
        ressemblance=extract(self.browser.body().inner_text,"ressemblance : ","% hors").strip()
        self.log("Taux de ressemblance identifié "+ressemblance)
        if int(ressemblance)>=seuil:
            suggest=self.find("aoukaColor suggest", 0)
            self.show(suggest, "OASIS propose par défaut un enregistrement proche")
            self.show(self.find("fsButton btn btn-default dropdown-toggle",0),"Il est possible de choisir un autre enregistrement pour la fusion")
            self.log("On réalise la fusion")
            self.click(suggest,"On teste l'enregistrement suggéré")
            self.show("table diffs dataTable no-footer","L'ensemble des champs impactés par la fusion sont listés ici")
            self.subtitle("Dans l'enregistrement fusionné, les champs rouges disparaissent au profit des champs 'verts'")
            if not self.fastMode:self.wait(1.5)
            rc=self.click("btn btn-primary btn-merge",0,text="On réalise la fusion")
            if not self.fastMode:self.wait(0.5)
        else:
            self.log("Ressemblance inférieur au seuil requis")
            rc = self.click("btn btn-default btn-close", 0, text="On annule la fusion")
            rc=False

        return rc

























