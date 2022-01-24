import datetime
import os
from random import randint

from mutagen.oggopus import OggOpus

def tirage( max,prefix=""):
    if type(max)==list:
        return prefix+max[randint(0, len(max))]
    else:
        return prefix+str(randint(0, max))


def digits(n_digits=10,start=""):
    for i in range(n_digits-len(start)):
        start=start+str(randint(0,10))
    return start


def words(n_words=10):
    bryant_words = """
                    this was the biggest disappointment of our trip the restaurant had received some very good reviews, so our expectations were high 
                    the service was slow even though the restaurant was not very full I had the house salad which could have come out of any sizzler in the us
                    the keshi yena although tasty reminded me of barbequed pulled chicken this restaurant is very overrated
                    """.split(" ")
    start = randint(0, len(bryant_words) - n_words)
    text:list=bryant_words[start:start + n_words]
    if ":" in text:text.remove(":")
    return " ".join(text)

def random_name():
    with open("firstnames.txt", "r") as myfile: data = myfile.readlines()
    s=data[int(tirage(len(data)))]
    return s.replace("\n","").lower()

def random_email():
    return random_name()+"."+random_name()+"@"+words(1)+".com"


def postal_address(prop:str=""):
    prop=prop.lower()
    if prop=="address":prop="adresse"
    txtAddress=tirage(999)+", rue de "+words(1)
    rc=dict({"adresse":txtAddress,"cp":tirage(99999),"ville":words(1),"town":words(1),"address":txtAddress});
    if prop=="all":return str(" ".join(rc.values()))
    if len(prop)==0 or not prop in rc:
        return rc
    else:
        return rc[prop]


def build_date(delay=15,format="dd/mm/YYYY"):
    now=datetime.datetime.now().timestamp()-delay*3600*24
    return datetime.datetime.fromtimestamp(now).strftime("%d/%m/%Y")



def getDuration(filename):
    if os.path.exists(filename):
        ogg=OggOpus(filename)
        if ogg is None:
            print("Problème avec le fichier "+filename)
        return ogg.info.length
    else:
        return 0




def extract(text:str,_from:str,_to:str):
    if _from in text:
        start=text.index(_from,0)
    else:
        start=0

    if _to in text:
        try:
            end=text.index(_to,start)
        except:
            end=len(text)
    else:
        end=len(text)

    if start==end:end=len(text)
    return text[start+len(_from):end]

