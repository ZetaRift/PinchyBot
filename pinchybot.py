#!/usr/bin/python2.7

import ch
import string
import os
import random
import time
import socket
import goslate
import settings
import sys
import datetime
import logging
import binascii
from random import randint
from bs4 import BeautifulSoup
from xml.dom import minidom
import derpi
import urllib2
import yt
import base64


logging.basicConfig(filename='PinchyBot.log',level=logging.DEBUG)

upt = time.time()   #To get the current unix time at execution



def urlparse(url):    #URL parsing for title. Needs BeauitfulSoup(3rd party)
    soup = BeautifulSoup(urllib2.urlopen(url))
    title = '<b>URL</b>: '+ soup.title.string
    ttitle = title.encode('ascii', 'ignore')
    return ttitle

def slate(tran, lang):
    gs = goslate.Goslate()
    tr = gs.translate(tran, lang)
    tr2 = tr.encode('utf8', 'strict')
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
    r2 = r2.strip(",")
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

def uptime():
    upd = time.time() - upt
    minu = int(upd / 60)   #Minutes
    hour = upd / 3600 #Hours
    return minu

class PinchyBot(ch.RoomManager):




  def onConnect(self, room):

    print("Connected to "+room.name)
    room.message("Hai!")

 

  def onReconnect(self, room):

    print("Reconnected to "+room.name)

  def onConnectFail(self, room):
      print("Failed to connect to "+room.name+ ", trying to reconnect..")
      room.reconnect()

 

  def onDisconnect(self, room):   #Wouldn't reconnect to the room unless you restart the script
    ctime = curtime()
    print("[" + ctime + "] Disconnected from" + room.name)
    
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
    self.safePrint("[" + ctime + "] " + room.name + ": "+user.name + ': ' + message.body) #Will print a timestamp next to the message

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

      elif cmd == 'diabetes':  #Random diabetes inducing poni image
       dia = random.choice(open('diabetes.txt', 'r').readlines())
       room.message(dia)

      elif cmd == 'ping':
       room.message('Pong')

      elif cmd == '8ball':
       rand = ['Yes', 'No', 'Outlook so so', 'Absolutely', 'My sources say no', 'Yes definitely', 'Very doubtful', 'Most likely', 'Forget about it', 'Are you kidding?', 'Go for it', 'Not now', 'Looking good', 'Who knows', 'A definite yes', 'You will have to wait', 'Yes, in my due time', 'I have my doubts']
       room.message(random.choice(rand))

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

      elif cmd == "lusers": #lists users in a chat room
       lst = ""
       lst = "<u>Users</u>:"
       for list in room.usernames:
        lst = lst + "<b>"+str(list)+"</b>"+", "
       room.message(lst, True)

      elif cmd == "otp":  #nowkiss.jpg
       u1 = user.name
       u2 = random.choice(room.usernames)
       if u2 == u1:
        room.message(u1+" x... Never mind..")
       else:
        room.message(u1+" x "+u2)

#      elif cmd == 'calc':   #Not really safe to use
#       try:
#        room.message(eval(str(args)))
#       except TypeError:
#        room.message("Wat.")
#       except NameError:
#        room.message("Math only, silly")
#       except SyntaxError:
#        room.message("I can't even understand..")
#       else:
#        room.message("Unsafe command")

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

      elif cmd == "setfont":  #Will set the font color, size, and the name color defined in the settings file
       status = readAdmin(user.name)
       if status == 1:
        self.setFontColor(settings.fontcolor)
        self.setNameColor(settings.namecolor)
        self.setFontSize(settings.fontsize)
        room.message("Done")


      elif cmd == "restart":   #Clones itself somehow
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
         score = derpi.score(args)
         uled = derpi.uled(args)
         tags = derpi.tagged(args)
         cmts = derpi.cmts(args)
         msg = "http://derpiboo.ru/"+args+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
         room.message(msg, True)
        except Exception as e:
         room.message("Image doesn't exist?")
         print(str(e))
       elif sw == "info":
         room.message("The !derpi.* command is a function that gets the stats off a derpibooru image using JSON, the available commands are: !derpi.img <image num ID> (Note: !derpi.img needs a moment to grab the stats), !derpi.tag <tag name>")
       elif sw == "tag":
        try:
         s1 = str(args.replace(" ", "+"))
         s1 = str(s1.replace(":", "-colon-"))
         tagct = derpi.tagsearch(args)
         searchlink = "http://derpiboo.ru/tags/"+s1
         msg = searchlink+" Tag <b>"+args+"</b> has "+tagct+" images"
         room.message(msg, True)
        except Exception as ee:
         emsg = "Tag <b>"+args+"</b>? That dosen't exist!"
         room.message(emsg, True)

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

      elif cmd == "reverse":  #Reversed text
       rev = str(args[::-1])
       room.message(rev)


      elif cmd.startswith("dex."):   #Pokedex, sends both a image of the pokemon and a link to it's stats.
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


      elif cmd == "quoteadd":   #Works.. kinda
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

      elif cmd == "uptime":
       u = str(uptime())
       room.message("Uptime: "+u+" minutes")



      elif cmd.startswith("help."):  #Help directive
       sw = cmd.split(".", 1)[1]
       hcmd = ['main', 'derpi', 'dex']
       if sw not in hcmd:
        room.message("Syntax: !help.directive (Available directives are: main, derpi, dex)")
       elif sw == 'main':
        room.message("General commands: !hug, !bestpony, !diabetes, !ping, !8ball, !dice, !google, !flipcoin, !lusers, !otp, !shiny")
       elif sw == 'derpi':
        room.message("The !derpi.* command is a function to print stats of an image from derpibooru. (See !derpi.info for available commands)")
        room.message("URLs matching http://derpiboo.ru/ or http://derpibooru.org/ with the image page will automatically be parsed.")
       elif sw == 'dex':
        room.message("National Pokedex. This function links an image of the pokemon, plus the link to its info. The available command is !dex.name <name of pokemon> (Exclude the brackets and do not use caps)")

#start of raw commands

    if message.body.startswith("http://derpiboo.ru/"):   #Added in try and except statment to avoid crashing on clash with non-image derpi URLs
     try:
      num = message.body.split("u/", 1)[1]
      score = derpi.score(num)
      uled = derpi.uled(num)
      tags = derpi.tagged(num)
      cmts = derpi.cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except Exception as e:
      print("Clashed with URL other than image page url, nothing to do ("+str(e)+")")

    if message.body.startswith("http://derpibooru.org/"):
     try:
      num = message.body.split("g/", 1)[1]
      score = derpi.score(num)
      uled = derpi.uled(num)
      tags = derpi.tagged(num)
      cmts = derpi.cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except:
      print("Clashed with URL other than image page url, nothing to do")

    if message.body.startswith("http://"):
     if message.body.startswith("http://derpibooru.org/"):  #We do not want the bot to parse two things at a time for derpi URLs
      print("Derpi URL")
     elif message.body.startswith("http://derpiboo.ru/"):
      print("Derpi URL")
     elif message.body.startswith("https://www.youtube.com/"):
      print("Youtube")
     elif message.body.startswith("http://www.youtube.com/"):
      print("Youtube")
     elif message.body.startswith("http://img.pokemondb.net/artwork/"):
      print("Pokedex")
     elif message.body.endswith(".jpg"):  #Will ignore image URLs
      print("Image.")
     elif message.body.endswith(".png"):
      print("Image.")
     elif message.body.endswith(".gif"):
      print("Image.")
     else:
      try:
       title = urlparse(message.body)
       room.message(title, True)
      except Exception as e:
       room.message("No title for URL?")
       print str(e)

    if message.body.startswith("https://"):   #https to http replacer
     url = message.body.replace("https://", "http://")
     room.message(url)

    if message.body.startswith(">>"):
     try:
      num = message.body.split(">>", 1)[1]
      score = derpi.score(num)
      uled = derpi.uled(num)
      tags = derp.tagged(num)
      cmts = derpi.cmts(num)
      msg = "http://derpiboo.ru/"+num+" | <b>Score</b>: "+score+" | <b>Comment count</b>: "+str(cmts)+" | <b>Uploaded by</b>: "+str(uled)+" | <b>Tags</b>: "+str(tags)
      room.message(msg, True)
     except:
      print("Clashed with URL other than image page url, nothing to do")

    if message.body.startswith("http://www.youtube.com/watch?v="):
     try:
      vid = message.body.split("watch?v=", 1)[1]
      views = yt.views(vid)
      length = yt.length(vid)
      length2 = yt.time(length)
      title = yt.title(vid)
      likes = yt.rateu(vid)
      dislikes = yt.rated(vid)
      msg = "Youtube video: "+title+" | Length: "+length2+" | Views: "+views+" | Likes: "+likes+" | Dislikes: "+dislikes
      room.message(msg, True)
     except Exception as e:
      print str(e)
       
#end of commands

  def onFloodBan(self, room):
    print("You are flood banned in "+room.name)

  def onPMMessage(self, pm, user, body):
    self.safePrint('PM: ' + user.name + ': ' + body)
    pm.message(user, "I am a bot, i will not respond to PMs. If you'd like to talk to my creator, then go here: http://crimsontail0.chatango.com/")

if __name__ == "__main__":  #Multiple rooms seperated by commas(each must be covered in quotation marks)
  PinchyBot.easy_start(settings.rooms, settings.nickname, settings.nickpass)

