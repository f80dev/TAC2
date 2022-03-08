from sys import argv

if "scenario" in argv:
    from lafaaac import LaFaaac
    tuto=LaFaaac()
    tuto.login("j.lecanu@femis.fr","123456789")
    tuto.open_module(1)

if "dataculture" in argv:
    from DataCultureUser import DataCultureUser

    #tuto=DataCultureUser(domain="https://testdcp.f80.fr",fastMode=False)


    tuto=DataCultureUser(argv[1],domain="http://localhost:4200/?no_auto_login",fastMode=False,quality=int(argv[2]))

    tuto.size(800,1000)

    tuto.capture("Search","Data Culture Pro","Recherche et édition des profils",background="https://testdcp.f80.fr/assets/img/anciens.jpg")
    tuto.intro(False)

    tuto.first_screen(comment=True)
    tuto.login("hhoareau@gmail.com","123456",quick=False)

    #tuto.edit_profil(0)

    tuto.explain_search()
    tuto.stop("Data Culture Pro","L'annuaire interractif des anciens élèves de la FEMIS",subdir="data_culture")

    tuto.capture("Stats","Data Culture Pro","Module statistiques")
    tuto.explain_statistic()
    tuto.stop("Data Culture Pro","L'annuaire interractif des anciens élèves de la FEMIS",subdir="data_culture")

    tuto.capture("EditProfil","Data Culture Pro","Consultation et édition des profils")
    tuto.search("sciamma")
    tuto.explain_fiche(0)
    tuto.edit_profil(0)
    tuto.stop("Data Culture Pro","L'annuaire interractif des anciens élèves de la FEMIS",subdir="data_culture")



    # tuto.add_experience("Comment je me suis disputé")
    # tuto.explain_fiche(0)
    # tuto.show_realisation()
    # tuto.quit("Data Culture Pro","L'annuaire interractif des anciens élèves de la FEMIS")
    #
    # tuto.capture("FonctionAnnexe","Data Culture Pro","Fonctions annexes",background="https://dcp.f80.fr/assets/img/anciens.jpg")
    # tuto.change_profil()
    # tuto.add_film()
    # tuto.show_statistique()
    tuto.close()


#f=FemisUser("j.lecanu","azerty")
from flyview import Flyview
from linkedinbot import LinkedinBot
from mural import Mural
from tutos_femis import TutoFemis
from utils import random_name

#f.capture("login","Première connexion","Utilisation du login et du mot de passe")

#f.delete_contact(type="CONTACT")



# tuto=LinkedinBot()
# tuto.start()
# tuto.open("hhoareau")
# s=tuto.export()
# print(s)


# tuto=Flyview()
# #tuto.buy_ticket()
# tuto.buy_gift_card()
# tuto.fill_infos()
# tuto.write_metrics()


if False:
    tuto=TutoFemis(prod=True)
    tuto.f.login("h.hoareau","Hh4271!!",False,False)
    tuto.create_profil("CONTACT",["sophie.dudule@gmail.com","paul.dudule@gmail.com","roger.legumes@gmail.com","rv@f80.fr","hhoareau@gmail.com","h.hoareau@femis.fr"])
    #tuto.scenario_inscription_sacre("paul","dudule","paul.dudule@gmail.com","Hh4271!!")
    #tuto.scenario_inscription_sacre("roger","legumes","roger.legumes@gmail.com","Hh4271!!")
    #tuto.scenario_creation_de_stage("Affectation d'un stage",1500)
    #tuto.f.delete_contacts("STUDENT","legumes","roger")

    # emails=[]
    # for i in range(0,15):emails.append({"email":"pro_"+random_name()+".dudule@gmail.com"})
    # tuto.create_profil("STUDENT_FC",emails)

    #tuto.scenario_mailing(_type="STUDENT_FI")

    #tuto.create_profil(type="PROF",profils=[{"email":"sophie.dudule@gmail.com","societe":"baxter"}])
    #tuto.create_stage()
    #tuto.scenario_societe()
    #tuto.dedoublonnage(["tcancelli","bcardinal","dcharron","achemin","echeyroux","kchir","hcohen","ccoucoureux","ecurtis","bdartois","ldecaster","cdelaunay","cdennebouy","adevillaire","adevulder","cdietrich","ydocouto","jdurif","lfanara","rfauvel","mfournier","lfrankias","cgalois","agneouchev","egodard","rgoldszal","ngoubet","ngrand","mhenochsberg","mhermelin","njactel","fkarimpour","vkeungkeosiane","skhoukh","rkirpicenko","llavalette","mlefeuvre","alejault","elevy","nlincy","mmancelneto","amaslah","tmatignon","mmilojevic","emommessin","emoreau","imorlat","smoundy","cneri","onovarese","ioger","molivier","eolounou","qpaquet","nparreaux","eparsegian","zpernet","cpezetamirat","cpin","apirotte","gplancquaert","hpokorny","lpu","hraffouldecomarmond","jrebena","ireille","treusa","jrevault","iriera","prigoux","mrolland","tropert","hrosseletruiz","mrossi","lrousseau","rseffacene","asoussana","jsquire","ksturm","asuzanne","steboul","otrably","furbani","sverge","mvettese","avigier","gvoigt","ealluynfride","janer","sangelini","lbapt","sbarandiaran","abargain","fbeillevaire","rbertino","mblancochaparro","aboileau","cboisivon"])
    #tuto.quit()




    #f.create_society(["ma societe","F80",0,"124564",0,0,"Informatique"])

pass



