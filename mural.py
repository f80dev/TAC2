from tools import Tools


class Mural(Tools):
    def __init__(self):
        super().__init__()
        self.start()
        self.fastMode=False


    def start(self):
        self.size(1400,1000)
        self.domain = "https://app.mural.co/"

    def login(self, username, password):
        self.go("https://app.mural.co/signin?ref=muralcoheader")
        self.subtitle("Pour commencer Mural nécessite un login et mot de passe, que vous obtenez en vous inscrivant à votre première connexion")
        self.clavier(username+"{{ENTER}}","input")
        elt_password=self.find("input",1)
        self.clavier(password+"{{ENTER}}",elt_password)
        return True

    def quit(self):
        self.stop("Bonne prise en main !", subtitle="Réalisation F80 (f80.fr)", subdir="mural")
        self.close()

    def open_template(self,index=1):
        self.subtitle("Nous allons vous présenter les principales fonctionnalités qui vous seront utiles, dans le cadre de l'atelier connecté Fresque du Climat")
        self.click("thumb-image-link",index-1)

    def explain_sidebar(self):
        self.wait(0.1)
        self.subtitle("Commençons par détailler la barre d'outils, à gauche de l'écran")
        texts=["Ajouter un post-it","Ajouter une forme ou une flèche","Ajouter un symbole","","Ajouter une image","","Dessiner"]
        for i in range(7):
            if len(texts[i])>0:
                elt=self.find("sidebar-button clickable",i)
                self.show(elt,texts[i],img="https://cdn.clipart.email/6b85ead069b73a56d6078488d84789e1_circle-draw-clipart_451-199.png")



    def explain_arrow_tools(self):
        self.wait(0.3)
        self.subtitle("Passons à la pratique")
        self.wait(0.1)
        self.subtitle("Comment créer une flèche ?")
        self.wait(0.2)
        self.click("sidebar-button clickable",1)
        self.subtitle("Les différents modèles de flèches apparaissent")
        self.show("mural-ui-tabs-shape-tab-list-item arrow-curve-thumb",
                  "Nous allons par exemple sélectionner cette flèche arrondie. Celle qui vous sera probablement la plus utile lors de l'atelier connecté",
                  img="https://cdn.clipart.email/6b85ead069b73a56d6078488d84789e1_circle-draw-clipart_451-199.png")
        self.click("mural-ui-tabs-shape-tab-list-item arrow-thumb",2)
        self.subtitle("Pour la faire apparaître sur l'espace de travail de la Fresque du Climat, il suffit de faire un glisser-déposer.")
        self.subtitle("Maintenez appuyé le clic gauche de votre souris, puis relâchez lorsque vous souhaitez déposer la flèche")
        self.subtitle("Une fois un élément déposé sur l'espace de travail de la Fresque du Climat")
        self.subtitle("il vous suffit de le sélecionner d'un clic,")
        self.subtitle("puis vous pourrez le déplacer, agrandir, rétrécir, tourner, etc autant que vous le voulez !")
        #self.video("https://interactive-examples.mdn.mozilla.net/media/examples/flower.webm",100,100,500,300,5)



