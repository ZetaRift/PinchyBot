#!/usr/bin/python2.6


#This bot requires the chatango library ch.py

import ch
import string
import os
import random
import time
import goslate
import settings
import sys
import datetime
import logging
import binascii
from random import randint
import urllib2
import json
from bs4 import BeautifulSoup
from xml.dom import minidom

logging.basicConfig(filename='PinchyBot.log',level=logging.DEBUG)



def urlparse(url):    #URL parsing for title. Needs BeauitfulSoup(3rd party)
    soup = BeautifulSoup(urllib2.urlopen(url))
    title = '<b>URL</b>: '+ soup.title.string
    return title

def slate(tran, lang):
    gs = goslate.Goslate()
    tr = gs.translate(tran, lang)
    tr2 = tr.encode('utf8', 'ignore')
    trf = tr2.decode('utf8', 'scrict')
    return tr2

def bestpone():
    pone = random.choice(open('bestpony.txt', 'r').readlines())
    return pone

def readAdmin(user):					
	bestand = open('admins.txt', 'r')
	for line in bestand:
		if user in line:
			status = 1
			return status
		else:
			status = 0
			return status

def roll(sides, count):
    r1 = str([randint(1, sides) for i in range(count)])
    r2 = r1.strip("[]")
    return r2


def curtime():
    ts = time.time()
    st = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    return st

def readRoom(room):					
	bestand = open('arooms.txt', 'r')
	for line in bestand:
		if room in line:
			rstatus = 1
			return rstatus
		else:
			rstatus = 0
			return rstatus

#Derpibooru JSON stuff, will add in tag search

def derpi_img_score(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    score = str(jso['score'])
    return score

def derpi_img_upvote(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upv = jso['upvotes']
    return upv

def derpi_img_downvote(num_id):    #Get score
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    upd = jso['downvotes']
    return upd

def derpi_img_uled(num_id): #Who uploaded the image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    uploader = jso['uploader']
    return uploader

def derpi_img_tagged(num_id): #Tags on a image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    tags = jso['tags']
    return tags

def derpi_img_cmts(num_id):  #Comment count of image
    url = urllib2.urlopen('https://derpiboo.ru/'+num_id+'.json')
    jso = json.load(url)
    cmts = jso['comment_count']
    return cmts


def derpi_total():
    url = urllib2.urlopen("http://derpiboo.ru/lists.json")
    jso = json.load(url)
    dat = jso['total_images']
    return dat
    

def derpi_tagsearch(tag):
    ser1 = str(tag.replace(" ", "+"))
    url = urllib2.urlopen("https://derpiboo.ru/tags/"+ser1+".json")
    jso = json.load(url)
    img_count = jso['tag']['images']
    return img_count

def dexname(name):
    xmldoc = minidom.parse("dex_xml/"+name+'.xml')
    dexname = xmldoc.getElementsByTagName('dexname')
    num = xmldoc.getElementsByTagName('num')
    typ = xmldoc.getElementsByTagName('typ') 
    hp = xmldoc.getElementsByTagName('hp') 
    atk = xmldoc.getElementsByTagName('atk')
    defe = xmldoc.getElementsByTagName('def')
    spa = xmldoc.getElementsByTagName('spa')
    spd = xmldoc.getElementsByTagName('spd')
    spe = xmldoc.getElementsByTagName('spe')
    tot = xmldoc.getElementsByTagName('tot')
    name = dexname[0].attributes['name'].value
    num = num[0].attributes['name'].value
    typ = typ[0].attributes['name'].value
    hp = hp[0].attributes['name'].value
    atk = atk[0].attributes['name'].value
    defe = defe[0].attributes['name'].value
    spa = spa[0].attributes['name'].value
    spd = spd[0].attributes['name'].value
    spe = spe[0].attributes['name'].value
    tot = tot[0].attributes['name'].value
    res = "Name: "+str(name)+" | Dex No: "+str(num)+" | Type: "+str(typ)+" | Health: "+str(hp)+" | Attack: "+str(atk)+" | Defense: "+str(defe)+" | Special Atk: "+str(spa)+" | Special Def: "+str(spd)+" | Speed: "+str(spe)+" | Total: "+str(tot)
    return res


def rpgstatc(lv, bs):
    flv = str(int(lv) * (0.01 * bs))
    return flv


def tempconv(pfix, value):
    if pfix == 'cf':
       tmp = value * 1.8 + 32
       return str(float(tmp))
    elif pfix == 'fc':
       tmp = (value - 32) * 5 / 9
       return str(float(tmp))
    elif pfix == 'ck':
       tmp = value + 273.15
       return str(float(tmp))
    elif pfix == 'kc':
       tmp = value - 273.15
       return str(float(tmp))


def imgspec(url):
    mime = ['.jpg', '.png', '.gif']
    i = urllib2.urlopen(url)
    return i.info()


def yt_views(vid_id):    #Get score
    url = urllib2.urlopen('http://gdata.youtube.com/feeds/api/videos/'+vid_id+'?alt=json')
    jso = json.load(url)
    views = str(jso['viewCount'])
    return views

def uhex(binary):
    n = int(binary, 2)
    nt = binascii.unhexlify('%x' % n)
    return nt

class PinchyBot(ch.RoomManager):




  def onConnect(self, room):

    print("Connected to "+room.name)
    room.message("Hai!")

 

  def onReconnect(self, room):

    print("Reconnected to "+room.name)

  def onConnectFail(self, room):
      print("Failed to connect to "+room.name+ ", trying to reconnect..")
      room.reconnect()

 

  def onDisconnect(self, room):

    print("Disconnected from "+room.name)
    
    room.reconnect()
    room.message("Nuu! Pinchy got disconnected")

  def onFloodWarning(self, room):
    room.setSilent(True)
    print("Flood warning for "+room.name+"!")



  def onJoin(self, room, user):
      ctime = curtime()
      self.safePrint("[" + ctime + "] " + user.name + " joined " + room.name)
      room.message(user.name + " has joined. Hai!")

  def onLeave(self, room, user):
      ctime = curtime()
      self.safePrint("[" + ctime + "] " + user.name + " left " + room.name)
    
 
  def onMessage(self, room, user, message):

    
    ctime = curtime()
    self.safePrint("[" + ctime + "] " + room.name + ": "+user.name + ': ' + message.body)

    if message.body[0] == "!":     #Command prefix

      data = message.body[1:].split(" ", 1)

      if len(data) > 1:

        cmd, args = data[0], data[1]

      else:

        cmd, args = data[0], " "

#start of commands
        

      if cmd == 'whoami':
       status = readAdmin(user.name)
       if status == 1:
        room.message('Bot admin')
       else:
        room.message('A puny user :3')

      elif cmd == 'join':
       status = readAdmin(user.name)
       if status == 1:
        self.joinRoom(args)
        logging.info("[" + curtime() + "] join command used by " + user.name + ", joined room " + args)

      elif cmd == 'part':
       status = readAdmin(user.name)
       if status == 1:
        self.leaveRoom(args)
        logging.info("[" + curtime() + "] part command used by " + user.name + ", left room " + args)

      elif cmd == "exec":
       status = readAdmin(user.name)
       if status == 1:
        try:
         exec(args)
        except:
         room.message("Nothing")

      elif cmd == "eval":
       status = readAdmin(user.name)
       if status == 1:
        try:
         logging.info("[" + curtime() + "] eval command used by " + user.name + ", trying to eval " + args)
         room.message(eval(args))
        except Exception as err:
         room.message('<b>Err:</b> ' + str(err), True)
      elif cmd == 'say':
       room.message(args)

      elif cmd == 'quiet':		#Command that the bot wont respond to any commands
       status = readAdmin(user.name)
       if status == 1:
        room.setSilent(True)
        logging.info("[" + curtime() + "] quiet command used by " + user.name + ", bot will no longer respond to general commands ")

      elif cmd == 'enable':
       status = readAdmin(user.name)
       if status == 1:
        room.setSilent(False)
        logging.info("[" + curtime() + "] enable command used by " + user.name + ", bot will respond to all commands")

      elif cmd == 'hug':
       room.message('*hugs ' + user.name + '*')

      elif cmd == 'bestpony':
       poni = bestpone()
       room.message(poni)

      elif cmd == 'diabetes':
       dia = random.choice(open('diabetes.txt', 'r').readlines())
       room.message(dia)

      elif cmd == 'ping':
       room.message('Pong')

      elif cmd == '8ball':
       rand = ['Yes', 'No', 'Outlook so so', 'Absolutely', 'My sources say no', 'Yes definitely', 'Very doubtful', 'Most likely', 'Forget about it', 'Are you kidding?', 'Go for it', 'Not now', 'Looking good', 'Who knows', 'A definite yes', 'You will have to wait', 'Yes, in my due time', 'I have my doubts']
       room.message(random.choice(rand))

      elif cmd == 'url.title':   #Not working atm
       room.message('The URL parser is not working at the moment')

      elif cmd == 'dice':
       try:
         number = int(args)
         thingy = str(random.randrange(1, number))
         room.message(thingy)
       except:
         room.message("It's not a number, silly")

      elif cmd == 'google':
       searcharg = str(args.replace(" ", "+"))
       searchlink = "http://www.google.com/#q="+searcharg
       room.message(searchlink)

      elif cmd == 'roll.2':
       di1 = str(random.randrange(0, 9))
       di2 = str(random.randrange(0, 9))
       tot = di1 + di2
       room.message('You rolled ' + di1 +' '+ di2)

      elif cmd == 'flipcoin':
       rand = ['Heads', 'Tails']
       room.message(random.choice(rand))   

      elif cmd == "lusers":
       lst = ""
       lst = "<u>Users</u>:"
       for list in room.usernames:
        lst = lst + "<b>"+str(list)+"</b>"+", "
       room.message(lst, True)

      elif cmd == "otp":
       u1 = user.name
       u2 = random.choice(room.usernames)
       if u2 == u1:
        room.message(u1+" x... Never mind..")
       else:
        room.message(u1+" x "+u2)

      elif cmd == 'calc':
       try:
        room.message(str(args))
       except TypeError:
        room.message("Wat.")
       except NameError:
        room.message("Math only, silly")
       except SyntaxError:
        room.message("I can't even understand..")
       else:
        room.message("Unsafe command")

      elif cmd == 'shiny':
       shi = str(random.randint(1,8192))
       if shi == 8192:
        room.message('You got shiny!')
       else:
        room.message('Nope (' + shi + '/8192)')


      elif cmd.startswith("goslate."):
       try:
        lang = cmd.split(".", 1)[1]
        trans = slate(args, lang)
        room.message(trans)
       except:
        synmsg = "<b>Syntax</b>: !goslate.language Text here (where language is the abbreviation like 'ru')"
        room.message(synmsg, True)

      elif cmd == "fontcolor":
       status = readAdmin(user.name)
       if status == 1:
        try:
         self.setFontColor(args)
        except:
         room.message("Wrong")

      elif cmd == "setfont":
       status = readAdmin(user.name)
       if status == 1:
        self.setFontColor(settings.fontcolor)
        self.setNameColor(settings.namecolor)
        self.setFontSize(settings.fontsize)
        room.message("Done")


      elif cmd == "restart":
       status = readAdmin(user.name)
       if status == 1:
        room.message("Restarting..")
        os.system("./rstart.py " + str(os.getpid()))

      elif cmd.startswith("echo."):
       sw = cmd.split(".", 1)[1]
       status = readAdmin(user.name)
       if status == 1:
        if sw == "on":
         ec = 0
         room.messafe("!say command is now usable by all users")
        elif sw == "botadmin":
         ec = 1
         room.message("!say command is now botadmin only")
        elif sw == "off":
         ec = 2
         room.message("!say command is disabled.")
        else:
         room.message("Switches are: on, botadmin, and off")

      elif cmd.startswith("derpi."):   #Derpibooru command
       sw = cmd.split(".", 1)[1]
       if sw == "img":
        try:
         score = derpi_img_score(args)
         uled = derpi_img_uled(args)
         tags = derpi_img_tagged(args)
         cmts = derpi_img_cmts(args)
         msg = "http://derpiboo.ru/"+args+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
         room.message(msg, True)
        except:
         room.message("Image doesn't exist?")
       elif sw == "info":
         room.message("The !derpi.* command is a function that gets the stats off a derpibooru image using JSON, the available commands are: !derpi.img <image num ID> (Note: !derpi.img needs a moment to grab the stats)")
       elif sw == "tag":
        try:
         s1 = str(args.replace(" ", "+"))
         tagct = str(derpi_tagsearch(args))
         searchlink = "http://derpiboo.ru/tags/"+s1
         msg = searchlink+" Tag <b>"+args+"</b> has "+tagct+" images"
         room.message(msg, True)
        except:
         room.message("Tag dosen't exist?")

      elif cmd == "fontsize":
       status = readAdmin(user.name)
       if status == 1:
        try:
         self.setFontSize(args)
        except:
         room.message("Wrong")

      elif cmd == "namecolor":
       status = readAdmin(user.name)
       if status == 1:
        try:
         self.setNameColor(args)
        except:
         room.message("Wrong")

      elif cmd == "reverse":
       rev = str(args[::-1])
       room.message(rev)


      elif cmd.startswith("dex."):   #Pokedex
       sw = cmd.split(".", 1)[1]
       if sw == 'name':
        try:
         urllib2.urlopen("http://pokemondb.net/pokedex/"+args)
         ps = "http://pokemondb.net/pokedex/"+args
         psp = "http://img.pokemondb.net/artwork/"+args+".jpg"
         room.message(psp+" "+ps)
        except:
         room.message("Dosen't exist (Don't use caps)")
       elif sw == 'gen1':
         room.message("#001-#151")
       elif sw == 'gen2':
         room.message("#152-#251")
       elif sw == 'gen3':
         room.message("#252-#386")
       elif sw == 'gen4':
         room.message("#387-#493")
       elif sw == 'gen5':
         room.message("#494-#649")
       elif sw == 'gen6':
         room.message("#650-#718")


      elif cmd == "quoteadd":
       status = readAdmin(user.name)
       if status == 1:
        with open('quotes.txt', 'a') as qfile:
         qfile.write(args)
         room.message("Added quote ("+args+") to file.")

      elif cmd == "quote":
       qmsg = random.choice(open('quotes.txt', 'r').readlines())
       room.message(qmsg)

      elif cmd == "sauce":
       rstatus = readRoom(room.name)
       if rstatus == 1:
        sauce = random.choice(open('sauce.txt', 'r').readlines())
        room.message(sauce)

      elif cmd == "lines":
       lct = str(len(open('pinchybot.py').readlines()))
       room.message("It takes "+lct+" lines to run PinchyBot!")

#start of raw commands

    if message.body.startswith("http://derpiboo.ru/"):   #Added in try and except statment to avoid crashing on clash with non-image derpi URLs
     try:
      num = message.body.split("u/", 1)[1]
      score = derpi_img_score(num)
      uled = derpi_img_uled(num)
      tags = derpi_img_tagged(num)
      cmts = derpi_img_cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except:
      print("Clashed with URL other than image page url, nothing to do")

    if message.body.startswith("http://derpibooru.org/"):
     try:
      num = message.body.split("g/", 1)[1]
      score = derpi_img_score(num)
      uled = derpi_img_uled(num)
      tags = derpi_img_tagged(num)
      cmts = derpi_img_cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except:
      print("Clashed with URL other than image page url, nothing to do")

    if message.body.startswith("http://"):
     if message.body.startswith("http://derpibooru.org/"):
      print("Derpi URL")
     elif message.body.startswith("http://derpiboo.ru/"):
      print("Derpi URL")
     elif message.body.startswith("http://img.pokemondb.net/artwork/"):
      print("Pokedex")
     elif message.body.endswith(".jpg"):
      print("Image.")
     elif message.body.endswith(".png"):
      print("Image.")
     elif message.body.endswith(".gif"):
      print("Image.")
     else:
      try:
       title = urlparse(message.body)
       room.message(title, True)
      except:
       room.message("No title for URL?")

    if message.body.startswith("https://"):   #https to http replacer
     url = message.body.replace("https://", "http://")
     room.message(url)

    if message.body.startswith(">>"):
     try:
      num = message.body.split(">>", 1)[1]
      score = derpi_img_score(num)
      uled = derpi_img_uled(num)
      tags = derpi_img_tagged(num)
      cmts = derpi_img_cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except:
      print("Clashed with URL other than image page url, nothing to do")
       
#end of commands

  def onFloodBan(self, room):
    print("You are flood banned in "+room.name)

  def onPMMessage(self, pm, user, body):
    self.safePrint('PM: ' + user.name + ': ' + body)
    pm.message(user, "I am a bot, i will not respond to PMs. If you'd like to talk to my creator, then go here: http://crimsontail0.chatango.com/")

if __name__ == "__main__":  #Multiple rooms seperated by commas(each must be covered in quotation marks)
  PinchyBot.easy_start(["pinchybott"], settings.nickname, settings.nickpass)

