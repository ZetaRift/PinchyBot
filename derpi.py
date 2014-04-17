import urllib2
import json

#Parse JSON data from a derpibooru image


def score(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    score = str(jso['score'])
    return score

def upvoted(num_id):    #Get upvotes
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upv = jso['upvotes']
    return upv

def downvoted(num_id):    #Get downvotes
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upd = jso['downvotes']
    return upd

def uled(num_id): #Who uploaded the image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    uploader = jso['uploader']
    return uploader

def tagged(num_id): #Tags on a image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    tags = jso['tags']
    return tags

def cmts(num_id):  #Comment count of image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    cmts = jso['comment_count']
    return cmts


def total():
    url = urllib2.urlopen("http://derpiboo.ru/images.json")
    jso = json.load(url)
    dat = jso['tag']['images']
    return dat
    

def tagsearch(tag):        #Searches for a tag
    ser1 = tag.replace(" ", "+")
    ser1 = ser1.replace(":", "-colon-")
    url = urllib2.urlopen("https://derpiboo.ru/tags/"+ser1+".json")
    jso = json.load(url)
    img_count = jso['tag']['images']
    return str(img_count)
