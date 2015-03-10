import requests
import json
import random


#Removed the nofav and nocomments parameters since they are now disabled by default
#Changed from urllib2 to requests (3rd party)
#Changes are being applied to the derpibooru API


def randcute():
    r = requests.get("http://derpibooru.org/tags/cute.json")
    jso = json.loads(r.text)
    dat = random.choice(jso['images'])
    iid = dat['id_number']
    return str(iid)
    

def tagsearch(tag):        #Dosen't work because it says "list indices must be integers, not str" on eval
    ser1 = tag.replace(" ", "+")
    ser1 = ser1.replace(":", "-colon-")
    r = requests.get("https://derpibooru.org/tags/"+ser1+".json")
    jso = json.loads(r.text)
    img_count = jso['tag']['images']
    return str(img_count)

def tagsp(tag):        #Returns URL of spoiler image, returns None (or null) if no url is present
    ser1 = tag.replace(" ", "+")
    ser1 = ser1.replace(":", "-colon-")
    r= requests.get("https://derpibooru.org/tags/"+ser1+".json")
    jso = json.loads(r.text)
    sp = jso['tag']['spoiler_image_uri_small']
    if sp is None:
     return None
    else:
     sp2 = "http:"+sp
     return sp2

def thumb(num_id):
    r = requests.get('http://derpibooru.org/'+num_id+'.json')
    jso = json.loads(r.text)
    sp = "http:"+jso['representations']['thumb']
    return str(sp)

def fetch_info(numid):
    r = requests.get('https://derpibooru.org/images/{num}.json'.format(num=numid))
    return json.loads(r.text)
 
_score = lambda img_info: int(img_info['score'])
_upv = lambda img_info: int(img_info['upvotes'])
_dwv = lambda img_info: int(img_info['downvotes'])
_faves = lambda img_info: int(img_info['faves'])
_cmts = lambda img_info: int(img_info['comment_count'])
_uled = lambda img_info: img_info['uploader']
_tags = lambda img_info: img_info['tags']
_chk_tags = lambda img_info: img_info['tag_ids']
_thumb = lambda img_info: "http:"+img_info['representations']['thumb']
_format = lambda img_info: img_info['original_format']

def stats_string(numid):   #something useless
    img_info = fetch_info(numid)
    if "explicit" in _chk_tags(img_info):
     return "<b>[Image is explicit]</b> http://derpibooru.org/{num} | <b>Score</b>: {score} ({upv} up / {dwv} down) with {faves} faves | <b>Comment count</b>: {cmts} | <b>Uploaded by</b>: {uled} | <b>Image #{num} tags</b>: {tags}".format(
         score=_score(img_info),
         upv=_upv(img_info),
         dwv=_dwv(img_info),
	 faves=_faves(img_info),
         cmts=_cmts(img_info),
         uled=_uled(img_info),
         tags=_tags(img_info),
	 num=numid
         )
    elif "questionable" in _chk_tags(img_info):
     return "<b>[Image is questionable]</b> http://derpibooru.org/{num} | <b>Score</b>: {score} ({upv} up / {dwv} down) with {faves} faves | <b>Comment count</b>: {cmts} | <b>Uploaded by</b>: {uled} | <b>Image #{num} tags</b>: {tags}".format(
         score=_score(img_info),
         upv=_upv(img_info),
         dwv=_dwv(img_info),
	 faves=_faves(img_info),
         cmts=_cmts(img_info),
         uled=_uled(img_info),
         tags=_tags(img_info),
	 num=numid
         )
    elif "grimdark" in _chk_tags(img_info):
     return "<b>[Image is grimdark]</b> http://derpibooru.org/{num} | <b>Score</b>: {score} ({upv} up / {dwv} down) with {faves} faves | <b>Comment count</b>: {cmts} | <b>Uploaded by</b>: {uled} | <b>Image #{num} tags</b>: {tags}".format(
         score=_score(img_info),
         upv=_upv(img_info),
         dwv=_dwv(img_info),
	 faves=_faves(img_info),
         cmts=_cmts(img_info),
         uled=_uled(img_info),
         tags=_tags(img_info),
	 num=numid
         )
    elif _format(img_info) == "gif":
     return "http://derpibooru.org/{num} | <b>Score</b>: {score} ({upv} up / {dwv} down) with {faves} faves | <b>Comment count</b>: {cmts} | <b>Uploaded by</b>: {uled} | <b>Image #{num} tags</b>: {tags}".format(
         score=_score(img_info),
         upv=_upv(img_info),
         dwv=_dwv(img_info),
	 faves=_faves(img_info),
         cmts=_cmts(img_info),
         uled=_uled(img_info),
         tags=_tags(img_info),
	 num=numid
         )
    else:
     return "{thumb} http://derpibooru.org/{num} | <b>Score</b>: {score} ({upv} up / {dwv} down) with {faves} faves | <b>Comment count</b>: {cmts} | <b>Uploaded by</b>: {uled} | <b>Image #{num} tags</b>: {tags}".format(
         score=_score(img_info),
         upv=_upv(img_info),
         dwv=_dwv(img_info),
	 faves=_faves(img_info),
         cmts=_cmts(img_info),
         uled=_uled(img_info),
         tags=_tags(img_info),
	 num=numid,
	 thumb=_thumb(img_info)
         )
