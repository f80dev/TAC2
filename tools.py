#Module dédié
#Syntaxe
#   - $$ permet de ne pas traduire le contenu
#   - ## exclue l'affichage pour le sous-titre
#   - !! exclue la voie du sous titre
import base64
import json
import os
import subprocess
from datetime import datetime

from os.path import exists
from random import randint, seed, random
from time import sleep

import mss
import unidecode
from google.cloud import texttospeech, translate_v2
from nerodia.browser import Browser
from selenium.webdriver import DesiredCapabilities, ActionChains
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import ProxyType, Proxy
from selenium.webdriver.remote.webdriver import WebDriver

import cv2
import numpy
from apscheduler.schedulers.background import BackgroundScheduler

from definitions import SUP_DELAY_SPEAK
from utils import getDuration


class Tools:

    fastMode=False
    metrics_cache=""
    browser=None
    dtStartCapture=None
    histo=list()

    fps=15 #réalisation du film a 15 images par secondes

    def __init__(self,proxy="",json_path="",speech_engine="fr-FR-Wavenet-A",translate_into="",subdir=""):
        self.showSubtitle = True
        self.translate_dict = None
        self.translate_engine = None
        self.source_language = "fr-FR"
        self.json_path = json_path
        self.set_subtitle_style()
        self.capture_file=""
        self.subdir = subdir
        if not exists("./"+subdir): os.mkdir("./"+subdir)

        self.translate_dict=dict()

        self.lang=translate_into #voir liste des langues acceptées : https://cloud.google.com/translate/docs/languages
        self.speech_engine=speech_engine
        self.client=None
        self.frames=[]
        self.player=None
        self.startLog=self.now()
        self.videoBatchFile=""

        capabilities = DesiredCapabilities.CHROME
        if len(proxy)>0:
            p = Proxy()
            p.proxy_type = ProxyType.MANUAL
            p.http_proxy = proxy
            p.socks_proxy = proxy
            p.ssl_proxy = proxy
            p.add_to_capabilities(capabilities)

        self.driver:WebDriver=WebDriver(command_executor="http://127.0.0.1:9515",desired_capabilities=capabilities)
        self.driver.implicitly_wait(1)
        self.browser:Browser = Browser(self.driver)
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()

    def set_subtitle_style(self,style="font-weight:bolder;font-size:large;color:yellow;padding: 5px;text-shadow: 0 0 2px #000;"):
        self.subtitle_style=style

    def back(self):
        self.browser.back()

    def init_zone_capture(self):
        offset = 125
        self.mon = {
            "top": self.browser.window().position.y + offset,
            "left": self.browser.window().position.x+10,
            "width": self.browser.window().size.width-10,
            "height": self.browser.window().size.height - offset - 5
        }

    def mobile(self,position=0,width=350):
        self.browser.window().move_to(position*width*1.5, 0)
        self.browser.window().resize_to(width, width * 4)
        self.init_zone_capture()

    def set_size(self,width=1000,height=800):
        self.browser.window().move_to(0, 0)
        self.browser.window().resize_to(width,height)
        self.init_zone_capture()

    def set_position(self,x=0,y=0,witdh=0,height=0):
        if witdh>0 and height>0:
            self.set_size(witdh,height)
        self.browser.window().move_to(x, y)
        self.init_zone_capture()

    def export(self,format="html"):
        if format=="html":
            return self.browser.html
        else:
            return self.browser.text

    def go(self,url:str=".",subtitle="",delay=0):
        if not url.startswith("http"):return False
        if self.browser.url==url:return True
        self.browser.goto(url)
        if len(subtitle)==0:
            self.wait(delay+1)
        else:
            self.subtitle(subtitle)
            self.wait(delay)
        return True


    def metrics(self, tag=""):
        if self.metrics_cache is None: self.metrics_cache = ""
        self.metrics_cache = self.metrics_cache + str(int(datetime.today().timestamp()*1000)) + ";" + tag + "\n"


    def write_metrics(self, filename=""):
        if len(filename) == 0:
            filename="session"+str(datetime.today().timestamp())

        if not filename.endswith(".csv"):filename=filename+".csv"

        with open(filename, "w") as text_file:
            text_file.write(self.metrics_cache)

        text_file.close()


    def scroll_down(self,target="main"):
        elt=self.driver.find_element_by_id(target)
        actions=ActionChains(self.driver)
        actions.key_down(Keys.PAGE_DOWN,elt).perform()


    def mouse_wheeldown(self,wheel=500):
        actions=ActionChains(self.driver)
        actions.move_by_offset(100,wheel)
        actions.perform()
        #self.browser.execute_script("setTimeout(function (){window.scroll(0,"+str(wheel)+");},20)")


    def getDelay(self,text: str):
        if self.fastMode:
            return 0
        else:
            sound_file=self.getSoundFile(text)
            return getDuration(sound_file)

            #n_words = len(text.split(" "))
            #return n_words * 300 + 1000


    def set_field(self,id=None,value=None,index=-1):
        if id is None:
            elt=self.browser.element()
        else:
            elt=self.find(id,index)

        if elt.tag_name=="input":
            if elt.attributes["type"]=="checkbox":
                if value:
                    elt.send_keys(Keys.SPACE)
                    self.add_click()
            else:
                self.clavier(value)

        if elt.tag_name=="select":
            if type(value)==str:elt.send_keys(value)
            if type(value)==int:
                for i in range(value):
                    elt.send_keys(Keys.ARROW_DOWN)

        return True


    def wait(self,nSecondes:float=5.0):
        if self.fastMode and nSecondes>3:nSecondes=3
        if nSecondes>0:
            sleep(nSecondes)


    def pere(self,elt):
        elt=self.find(elt)
        if not elt is None:return elt.element(xpath="..")
        return None



    def findall(self, name, pere=None):
        if pere is None: pere = self.browser
        objs = pere.elements(name=name)
        return objs




    def find(self,id,index=None,pere=None,onlyId=False,onlyName=False):
        if pere is None:pere=self.browser
        obj=None
        if type(id)==str:
            if onlyId:
                return pere.element(id=id)

            objs=pere.elements(name=id)
            if not onlyName and len(objs)==0:
                objs=pere.elements(class_name=id)
                if len(objs)==0: objs = pere.elements(tag_name=id)



            if type(index)==str:
                #On cherche par rapport au contenu
                for obj in objs:
                    if str(obj.text).startswith(index):
                        return obj
            else:
                if not index is None and index<=len(objs):
                    obj=objs[index]

            if obj and not obj.exist:return None
            return obj
        else:
            #L'objet à trouvé à directement été passé en argument
            return id


    def size(self, width, height):
        self.browser.window().resize_to(width,height)
        self.init_zone_capture()


    def showImage(self,src,style="width:100vw;object-fit:cover",subtitle=""):
        delay=self.speak(subtitle)
        if delay<1:delay=1
        self.execute("showImages",src,delay,style)
        self.subtitle(subtitle)


    def click(self,id,index=0,timeout=0.2,text=""):
        obj=self.find(id,index)
        if obj is None:return False
        if len(text)>0:
            self.show(obj,text)

        self.pointElement(obj)
        try:
            self.wait(0.2)
            obj.click()
            self.add_click()
            self.wait(timeout)
        except:
            self.log(str(id)+" est non clickable")
            return False

        return True


    def video(self,src,top=0,left=0,width="100vw",height="100vh",delayInSec=3,new_window=False):
        if new_window:
            videoBrowser = Browser(WebDriver())
            videoBrowser.title=""
            videoBrowser.status=""
            videoBrowser.original_window.position.x=self.browser.window().position.x+left
            videoBrowser.original_window.position.y = self.browser.window().position.y + top
            videoBrowser.original_window.size.width=width
            videoBrowser.original_window.size.height= height
            self.execute("playVideo", src, 0, 0, "100vw", "100vh", delayInSec * 1000,videoBrowser)
        else:
            self.execute("playVideo",src,top,left,width,height,delayInSec*1000)

        self.wait(delayInSec)



    def capture(self,filename="",title="",subtitle="",background="black"):
        """

        :param name:
        :param title:
        :param subtitle:
        :return:
        """

        if len(filename)==0:
            filename=unidecode.unidecode(title.replace(" ","_").replace("'","_").replace("é","e").replace("$$",""))
            self.log("Génération du nom de fichier depuis le titre : "+filename)

        if len(self.capture_file)>0:self.stop(10)
        self.log("Démarage de la capture pour le fichier " + filename)

        self.capture_file=filename
        with mss.mss() as self.sct:
            self.sct.compression_level = 2

        interval_en_minutes=1/(self.fps*60)


        self.scheduler.add_job(self.job_capture,"interval",minutes=interval_en_minutes,max_instances=1,id="capture_job")
        self.dtStartCapture = self.now()
        self.fastMode=False

        if len(title)>0:
            self.insertCache("black", id_cache="cache_capture", position=9999,delayInSec=0.1)
            self.title(title,subtitle=subtitle,background=background)
            self.removeCache(id_cache="cache_capture")





    def fill_form(self,values,first=None,validate=None,comments=[]):
        if not first is None:
            if first=="{{TAB}}":
                self.browser.send_keys(Keys.TAB)
            else:
                self.focus(self.find(first,0))

        index=0
        iComments=0
        comments=comments+[""]*(len(values))
        for val in values:
            #Selection dans une liste déroulante
            if type(val)==int and val>0:
                self.browser.send_keys(Keys.ENTER)
                for i in range(val):
                    if not self.fastMode:self.wait(0.2)
                    self.browser.send_keys(Keys.ARROW_DOWN)
                if not self.fastMode: self.wait(0.3)
                self.browser.send_keys(Keys.ENTER)

            if type(val)==bool:
                self.subtitle(comments[iComments])
                self.browser.send_keys(Keys.SPACE)

            if type(val) == list:
                elt = self.driver.switch_to.active_element
                self.show(elt, comments[iComments])
                self.browser.send_keys(Keys.ENTER)
                self.select_in_list(val,multi=True)

            if type(val)==str:
                if val.startswith("list:"):
                    elt=self.driver.switch_to.active_element
                    self.show(elt,comments[iComments])
                    self.browser.send_keys(Keys.ENTER)
                    self.select_in_list(list((val.split("list:")[1]).split(",")))

                    #On reparcours la liste des élements
                    self.find(first, 0).focus()
                    for k in range(index):
                        self.browser.send_keys(Keys.TAB)
                else:
                    if len(val)>0:
                        if val=="{{TAB}}" or val=="{TAB}" or val=="TAB":
                            self.browser.send_keys(Keys.TAB)
                        else:
                            if val.startswith("name:"):
                                self.click(val.split("=")[0].replace("name:",""))
                                val=val.split("=")[1]
                            self.clavier(val,subtitle=comments[iComments])
                            self.browser.send_keys(Keys.CONTROL+"s")

            iComments=iComments+1

            if not self.fastMode:self.wait(0.5)

            index=index+1
            #On passe au champs suivant
            if index < len(values): self.browser.send_keys(Keys.TAB)

        if not validate is None:
            if type(validate)==str and "ENTER" in validate:
                self.browser.send_keys(Keys.ENTER)
                return True
            else:
                return self.click(validate,0)


    def escape(self):
        self.clavier("{{ESC}}")


    def clavier(self,text,elt=None,subtitle="",waitInSec=0,show=True):
        if len(text)==0:return False
        if len(subtitle)>0:
            if show:
                self.show(elt,subtitle)
            else:
                self.subtitle(subtitle)

        if not elt is None:
            if type(elt)==str:
                elt=self.find(elt,0)
            if not elt is None:elt.focus()

        text = text.replace("{{ENTER}}",chr(8)+Keys.ENTER)
        text = text.replace("{{TAB}}", Keys.TAB)
        text = text.replace("{{ESC}}", Keys.ESCAPE)
        text = text.replace("{{DOWN}}", Keys.ARROW_DOWN)
        text = text.replace("{{PAGEDOWN}}", Keys.PAGE_DOWN)
        text = text.replace("{{UP}}", Keys.ARROW_UP)
        text = text.replace("{{ESCAPE}}", Keys.ESCAPE)
        text = text.replace("{{WAIT}}", chr(8))

        dtStart = self.now()
        for ch in text:
            if ch==chr(8):
                self.wait(0.5)
            else:
                self.wait(randint(0,100)/5000)
                self.browser.send_keys(ch)

        self.add_sound("./clavier.wav",  (self.now() - dtStart), 0.6, 0, 0, 0)
        self.wait(waitInSec)

        return True





    def select_in_list(self,elt,indexes,filter="",multi=True):
        """

        :param index:
        :return:
        """

        if type(indexes)!=list:indexes=[indexes]

        # if type(indexes[0])==str:
        #     filter=indexes[0]
        #     del indexes[0]
        #     if len(indexes)==0:indexes.append(1)

        zone_filter = self.find(elt, index=0)
        if len(filter)>0:
            self.show(zone_filter,"Afin de simplifier le choix dans la liste, il est possible de réduire le nombre d'éléments via la zone de filtre")
            zone_filter.focus()

            self.browser.send_keys(Keys.CONTROL+"a")
            self.clavier(filter)
            self.wait(0.5)
            if multi:self.clavier("{{ENTER}}")
            self.subtitle("La liste se réduit dés les premiers caractére saisie dans le filtre")
        else:
            zone_filter.focus()

        if multi:
            l_index=list()
            for ch in indexes:
                l_index.append(int(ch))

            l_index.sort()

            self.subtitle("On peut sélectionner tous les éléments de la liste ou n'en prendre que certains grâce aux case à cocher")
            for i in range(max(l_index)+1):
                self.browser.send_keys(Keys.TAB)
                if i in l_index:
                    self.browser.send_keys(Keys.SPACE)
                    self.add_click()
                if not self.fastMode:self.wait(0.1)

                if not self.fastMode:self.wait(0.3)
            self.wait(1)
            self.click_at(50, 50)
        else:
            elt=self.find("label",indexes[0])
            self.click(elt)




    def click_at(self,x,y,subtitle=""):
        pyautogui.click(self.browser.window().position.x + x,self.browser.window().position.y+100+y)
        self.subtitle(subtitle)




    def fill_form_old(self, zone, vals, submit):
        _zone=self.find(zone,0)
        elts_to_fill=list()
        for elt in _zone.elements(tag_name="input"):
            if elt.visible:
                elts_to_fill.append({"elt":elt,"position":elt.location.y})

        for elt in _zone.elements(tag_name="select"):
            elts_to_fill.append({"elt":elt,"position":elt.location.y})

        elts_to_fill=sorted(elts_to_fill,key=lambda elt:elt["position"])

        i=0
        for elt in elts_to_fill:
            self.set_field(elt["elt"].id,vals[i])
            i=i+1
            if i>=len(vals):break

        return self.click(submit)


    def nav(self, param):
        return param in self.browser.url




    def stop(self,title="",subtitle="",offset=0,subdir="",extension="webm"):
        if len(subdir)>0:self.subdir=subdir
        if len(self.frames)==0:return False
        if len(title)>0:
            self.title(title,subtitle=subtitle,removeCache=False)

        self.log("Fin de la capture")
        self.scheduler.remove_job(job_id="capture_job")
        video = cv2.VideoWriter('./'+self.capture_file+'.avi',
                                cv2.VideoWriter_fourcc(*'XVID'),
                                self.fps,
                                (self.mon["width"], self.mon["height"])
                                )
        self.removeCache()

        self.log("Encodage de "+str(len(self.frames))+" images")
        for frame in self.frames:
            offset=offset-1
            if offset<0:video.write(frame)

        video.release()
        cv2.destroyAllWindows()

        self.log("Production du fichier BAT de génération du film")

        #format = self.videoBatchFile.substring(videoFile.lastIndexOf(".") + 1).toLowerCase().trim();
        #new_name = self.videoBatchFile.replace("tags", tags.replace("#", "")).replaceAll(" ", "_").replaceAll("_temp", "");

        # -c copy
        self.videoBatchFile =self.videoBatchFile + "\ndel \""+self.capture_file+"."\
                             +extension+"\"\nffmpeg -i \"" + self.capture_file+".avi" \
                             + "\" -i input.wav -c:v libvpx-vp9 -crf 30 -b:v 0 "+self.capture_file+"."+extension+"\n"
        #TODO le lancement de la vidéo ne fonctionne pas
        #self.videoBatchFile = self.videoBatchFile +"\ncall \""+self.capture_file+".mkv\""

        if len(self.subdir)>0:
            if not os.path.exists("./"+self.subdir):os.mkdir("./"+self.subdir)
            self.videoBatchFile=self.videoBatchFile +"\nMOVE /Y "+self.capture_file+".* "+self.subdir

        with open(self.capture_file+".bat", "w") as text_file:
            text_file.write(self.videoBatchFile)

        subprocess.run([self.capture_file+".bat"])

        self.frames=list()
        self.histo=list()





    def close(self):
        if self.scheduler.running:
            self.scheduler.shutdown()




    def job_capture(self):
        img = numpy.array(self.sct.grab(self.mon))
        img = numpy.flip(img[:, :, :3], 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.frames.append(img)



    def waitFor(self, elt,timeout=10,disapear=False):
        for essai in range(timeout):
            self.wait(1)
            obj=self.find(elt)
            if (not disapear and not obj is None) or (disapear and obj is None):
                return True

        return False


    def waitForURL(self, text,timeout=10,disapear=False):
        for essai in range(timeout):
            if (not disapear and text in self.browser.url) or (disapear and not text in self.browser.url):
                return True
            self.wait(1)

        return False

    def get_from_translate_dict(self,text,lang=None):
        if lang is None:lang=self.lang
        if text.startswith("$$"): return text.replace("$$","")
        text=text.replace("##","").replace("!!","")
        if self.translate_dict is None:
            dict_file="./"+self.subdir+"/translate_dict.json"
            if not exists(dict_file):
                self.translate_dict=dict()
            else:
                with open(dict_file,"r",encoding="utf8") as inputfile:
                    self.translate_dict=json.load(inputfile)

        if text in self.translate_dict and lang in self.translate_dict[text]: return self.translate_dict[text][lang]

        return None


    def add_to_translate_dict(self,text,translate_text,lang=None):
        if lang is None:lang=self.lang
        if not text in self.translate_dict:self.translate_dict[text]=dict()
        text=text.replace("##","").replace("!!","")
        self.translate_dict[text][lang]=translate_text.replace("##","").replace("!!","")
        dict_file="./"+self.subdir+"/translate_dict.json"
        with open(dict_file, "w",encoding='utf8') as outfile:
            json.dump(self.translate_dict,outfile,ensure_ascii=False)




    def translate(self,text,to_lang=None,src_lang=None):
        if to_lang is None:to_lang=self.lang
        if src_lang is None:src_lang=self.source_language

        rc={"translatedText":self.get_from_translate_dict(text,to_lang)}
        if rc["translatedText"] is None and to_lang!="":
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=self.json_path
            if self.translate_engine is None:
                #voir https://googleapis.dev/python/translation/latest/translate_v3/translation_service.html
                self.translate_engine = translate_v2.Client(to_lang.split("-")[0]) #https://cloud.google.com/translate/docs/languages
            try:
                rc=self.translate_engine.translate(text.replace("!!","").replace("##",""),target_language=to_lang.split("-")[0], source_language=src_lang.split("-")[0],model="base")
                if text.startswith("!!"):rc["translatedText"]="!!"+rc["translatedText"]
                if text.startswith("##"):rc["translatedText"]="##"+rc["translatedText"]
                self.add_to_translate_dict(text,rc["translatedText"],to_lang)
            except Exception as inst:
                self.log("Probleme de traduction "+str(inst.args))
                pass

        return rc["translatedText"]



    def speak(self,text: str):
        """

        :param text:
        :param output_filename:
        :return:
        """
        if self.fastMode or self.dtStartCapture is None or len(text)==0 or text.startswith("!!"):return 0.5

        output_filename = self.getSoundFile(text)

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=self.json_path
        if not exists(output_filename):
            if self.client is None:
                self.client = texttospeech.TextToSpeechClient()

            #Liste des moteurs
            synthesis_input = texttospeech.SynthesisInput(ssml=text.replace("!!","").replace("##","").replace("$$",""))
            voice = texttospeech.VoiceSelectionParams(name=self.speech_engine, language_code=self.lang+"-"+self.lang.upper(),
                                                      ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
            #
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)
            try:
                self.log("Vocalisation de la phrase " + text)
                response = self.client.synthesize_speech(input=synthesis_input,voice=voice, audio_config=audio_config)
                # The response's audio_content is binary.
                with open(output_filename, 'wb') as out:
                    # Write the response to the output file.
                    out.write(response.audio_content)
                    out.close()

            except Exception as inst:
                self.log("Probléme de génération du fichier "+str(inst.args))

        delay = getDuration(output_filename) + SUP_DELAY_SPEAK

        timecode=int((self.now()-self.dtStartCapture)*1000)
        code="\necho(\"Insertion de '"+text+'" de '+str(timecode/1000)+" sur "+str(delay)+" secondes\")\n"
        if "input.wav" not in self.videoBatchFile:
            code = code+"\ndel input.wav\nffmpeg -f lavfi -i anullsrc=channel_layout=1:sample_rate=48000 -t " + str(timecode/1000) + " input.wav\n"

        code = code + "del output.wav\n"
        code=code+"call ffmpeg -i input.wav -acodec libopus -i "+output_filename+" -filter_complex \"[0:a]volume=1[a0];[1:a]adelay=%delay%,volume=1[a1];[a0][a1]amix=inputs=2,volume=2[a]\" -map \"[a]\" output.wav\n"
        code = code + "\ndel input.wav\ncopy output.wav input.wav\n"

        code = code.replace("%delay%",str(timecode) + "|" + str(timecode))
        self.videoBatchFile = self.videoBatchFile+code + "\n"

        return delay




    def add_sound(self,file,  durationInSec, volume, offsetInSec, start_fadeout,delay_fadeout):
        """
        Ajout d'un effet sonor
        :param file:
        :param startInMilliseconds:
        :param durationInSec:
        :param volume:
        :param offsetInSec:
        :param start_fadeout:
        :param delay_fadeout:
        :return:
        """
        if self.dtStartCapture is None:return False

        timecode=int((self.now()-self.dtStartCapture)*1000)-300

        sOffset = "-ss " + str(offsetInSec)
        if offsetInSec == 0:sOffset="";

        sDuration = "-t " + str(durationInSec)
        if durationInSec == 0:sDuration=""

        code="\necho 'Ajout de "+file+" à la position "+str(timecode)+"'\n"
        code=code+"\ndel output.wav\ncall ffmpeg -y "+sOffset+" -i "+file+" "+sDuration+" -c copy output_insert.wav\n"
        code=code+"call ffmpeg -y -i input.wav -i output_insert.wav -filter_complex \"[0:a]volume=1[a0];[1:a]adelay="
        code=code+str(timecode)+"|"+str(timecode)+",volume="+str(volume)+"[a1];[a0][a1]amix=inputs=2,volume=2[a]\" -map \"[a]\" output_temp.wav\n"

        if start_fadeout > 0:
            code = code + "ffmpeg -i output_temp.wav -af \"afade=t=out:st=" + str(start_fadeout) + ":d=" + str(delay_fadeout) + ":curve=tri\" output.wav\n"
        else:
            code = code + "copy output_temp.wav output.wav\n"

        code = code + "\ndel input.wav\ncopy output.wav input.wav\ndel output_insert.wav\n\n\n"

        self.videoBatchFile =self.videoBatchFile+ code
        return True


    def getSoundFile(self,text:str):
        return "./"+self.subdir+"/voice_" + str(text.__hash__())+"_"+self.speech_engine+".ogg"


    def subtitle(self,text,position="90vh",_async=False,force=False):
        total_delay=0
        for txt in text.split("|"):
            txt=self.translate(txt)
            if not txt in self.histo:
                self.log(txt)
                self.histo.append(txt)
                if position=="top":position="10vh"
                delay = self.speak(txt)
                if txt.startswith("!!"):txt=txt.replace("!!","")
                if force or (not txt.startswith("##") and self.showSubtitle):
                    self.execute("showSubtitle",txt,delay*1000,self.subtitle_style,position)
                if not _async:self.wait(delay)
                total_delay=total_delay+delay

        return total_delay

    def show(self,id,text="",img="https://www.propizi.com/images/home/hero_shape.svg",scale=1.1):
        """

        :param id:
        :param text:
        :return:
        """
        delay=0
        if not self.fastMode and len(text)>0:
            elt=self.find(id,0)
            if not elt is None and not text in self.histo:
                if len(text)==0: text=elt.get_attribute("title")
                delay=self.subtitle(text,_async=True)
                w = elt.size.width
                h = elt.size.height
                if w<50 or h<40:scale=scale*1.3

                marge_x=(scale-1)*w/2
                marge_y=(scale-1)*h/2
                x=elt.location.x-marge_x
                y=elt.location.y-marge_y
                try:
                    self.execute("showElement", x,y,w*scale,h*scale, img,delay*1000)
                except:
                    pass
                self.wait(delay)
        return delay



    def title(self,title,subtitle="",style="color:white",background="black",removeCache=True):
        """

        :param title:
        :param subtitle:
        :param style:
        :param background:
        :return:
        """
        subtitle=self.translate(subtitle)
        title=self.translate(title)
        id_cache="cache_"+str(self.now())
        if not self.fastMode and not title in self.histo:
            if len(background)>0:
                self.insertCache(background,id_cache=id_cache,position=10000)
                self.wait(0.5)

            self.histo.append(title)

            to_speak=title
            if len(subtitle)>0:to_speak=to_speak+".<break time=\"0.2s\"/>"+subtitle

            delay=self.speak("<speak>"+to_speak+"</speak>")
            if delay<3:delay=3
            self.execute("showTitle",title.replace("!!",""),subtitle,delay*1000+500,style)
            self.wait(delay-1)

            if len(background) > 0 and removeCache:
                self.removeCache(id_cache=id_cache)
                self.wait(0.5)



    def pointElement(self,obj):
        x=obj.location.x+obj.size.width/2
        y=obj.location.y+obj.size.height/2
        self.execute("pointElement",x,y,500)
        if not self.fastMode:self.wait(0.5)


    def execute(self,file,*args):
        with open("js/"+file+".js", "r") as myfile:
            data= "".join(myfile.readlines())

        browserToExecute=self.browser

        i=0
        for arg in args:
            if type(arg)==Browser:
                browserToExecute=arg
            else:
                i=i+1
                data=data.replace("#"+str(i),str(arg))

        result=browserToExecute.execute_script(data)
        return result


    def select(self, elt, value):
        if type(elt)==str:
            obj=self.browser.select(id=elt)
        else:
            obj=elt

        if obj is None:return False
        if obj.exists:
            if type(value)==int:
                for i in range(value):
                    obj.send_keys(Keys.ARROW_DOWN)
            else:
                obj.select(value)
            return True
        return False



    # Retourne la date du jour en secondes
    def now(self):
        rc = datetime.now(tz=None).timestamp()
        return rc

    def log(self,text: str, sep='\n'):
        if not text is None:
            line: str = str(int(self.now() - self.startLog)) + " : " + text
            print(line)
            #store_log = line + sep + store_log[0:10000]
        return text

    def maximize(self):
        self.browser.window().maximize()
        self.init_zone_capture()

    def imageToBase64(self,filename:str):
        with open(filename, "rb") as image_file:
            data=base64.b64encode(image_file.read())

        ext=filename[filename.rindex(".")+1:]
        return "data:image/"+ext+";base64,"+str(data,"utf8")


    def insertCache(self,background:str="black",image="",delayInSec=1,position=1000,id_cache="",size="cover"):
        if len(image)>0:
            style = "background:center / "+size+" no-repeat url('" + image + "');background-color:"+background+";)"
        else:
            style = "background-color:" + background
        self.execute("insertCache",delayInSec,style,position,id_cache)


    def removeCache(self,id_cache="TAC_cache",delayInSec=1):
        self.execute("removeCache",id_cache,delayInSec)
        self.wait(delayInSec)



    def add_click(self):
        self.add_sound("./click.mp3", 0.2, 0.6, 0, 0, 0)

    def focus(self, node):
        if node is None:return False
        node.focus()
        return True

