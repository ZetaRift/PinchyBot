#!/usr/bin/python2.7


#PinchyBot for chatango

#This requires the following 3rd party python libraries as of current: requests and BeautifulSoup

#Unicode sending issue fixed in ch.py at 2015-03-03

import ch
import string
import os
import random
import time
import socket
import settings
import sys
import datetime
import logging
import binascii
from random import randint
from bs4 import BeautifulSoup
from xml.dom import minidom
import urllib2
import requests
import thread
import json
from datetime import timedelta
import decimal
import hashlib
import traceback
from functions import *   #This imports the functions such as derpi, wz, yt

version_string = "beta 0.7.6"


dish = 0

echo = 0

greetmsg = True  #Greet is enabled by default, which means the bot will greet a user joining a room

logging.basicConfig(filename='PinchyBot.log',level=logging.DEBUG)

upt = time.time() #Grab current unix time upon execution








def urlparse(url):    #URL parsing for title. Needs BeauitfulSoup and requests, both are 3rd party
    r = requests.get(url)
    soup = BeautifulSoup(r.text)
    title = '[ '+ soup.title.string+" ]"
    ttitle = title.encode('ascii', 'ignore')
    return ttitle

def slate(tran, lang):
    gs = goslate.Goslate()
    tr = gs.translate(tran, lang)
    return tr


def readAdmin(user): #Boolean values are better in this case, and on similar defs
	f = open('admins.txt', 'r')
	for line in f:
		if user in line:
			status = True
			return status
		else:
			status = False
			return status

def roll(sides, count):
    r1 = str([randint(1, sides) for i in range(count)])
    r2 = r1.strip("[]")
    r2 = r2.replace(", ", " ")
    return r2


def curtime(): #Return string of current time in Y-m-D H:M:S format
    ts = time.time()
    st = str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
    return st

def tstamp(t): #Return string of human-readable time from unix time
    st = str(datetime.datetime.fromtimestamp(float(t)).strftime('%Y-%m-%d %H:%M:%S'))
    return st

def readRoom(room):					
	bestand = open('arooms.txt', 'r')
	for line in bestand:
		if room in line:
			rstatus = True
			return rstatus
		else:
			rstatus = False
			return rstatus

def blist(user):					
	bestand = open('blist.txt', 'r')
	for line in bestand:
		if user in line:
			rstatus = True
			return rstatus
		else:
			rstatus = False
			return rstatus


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

def uhex(binary):
    n = int(binary, 2)
    nt = binascii.unhexlify('%x' % n)
    return nt

def uptime():
    upd = time.time() - upt
    tz = str(timedelta(seconds=upd))
    tz = tz.split(".")[0]
    return tz


def UserMetric(user):					
	bestand = open('user_metric.txt', 'r')
	for line in bestand:
		if user in line:
			mstatus = 1
			return mstatus
		else:
			mstatus = 0
			return mstatus


def wmetric(user):
 with open("wz-data.json", 'r') as f:
  jso = json.load(f)
  rt = jso['users'][user]['metric']
  return rt

def wzip(user):
 with open("wz-data.json", 'r') as f:
  jso = json.load(f)
  rt = jso['users'][user]['zip']
  return rt

def wexist(user):
 try:
  with open("wz-data.json", 'r') as f:
   jso = json.load(f)
   rt = jso['users'][user]
   return 1
 except:
   return 0

def ignoreurl():
 print("URL ignored.")


class PinchyBot(ch.RoomManager):  #Main class




  def onConnect(self, room):

    print("Connected to "+room.name)
    self.setFontColor(settings.fontcolor)
    self.setNameColor(settings.namecolor)
    self.setFontSize(settings.fontsize)

 

  def onReconnect(self, room):

    print("Reconnected to "+room.name)

  def onConnectFail(self, room):
      print("Failed to connect to "+room.name+ ", trying to reconnect..")
      room.reconnect()

 

  def onDisconnect(self, room):   #Wouldn't reconnect to the room unless you restart the script
    ctime = curtime()
    print("[" + ctime + "] Disconnected from " + room.name)
    
    self.joinRoom(room.name)
    room.message("Nuu! Pinchy got disconnected")

  def onFloodWarning(self, room):
    room.setSilent(True)
    print("Flood warning for "+room.name+"!")



  def onJoin(self, room, user):
      ctime = curtime()
      self.safePrint("[{ts}] {user} joined {room}".format(ts=ctime,user=user.name,room=room.name))
      global greetmsg
      if greetmsg == True:
       room.message("{user} has joined, hi!".format(user=user.name))
      else:
       print("Greet omitted")

  def onLeave(self, room, user):
      ctime = curtime()
      self.safePrint("[{ts}] {user} left {room}".format(ts=ctime,user=user.name,room=room.name))
    
 
  def onMessage(self, room, user, message):
     
     

    rstatus = blist(user.name) #Checks if a user is blacklisted from the bot
    if rstatus == True:
     room.setSilent(True)
    else:
     room.setSilent(False)
    ctime = curtime()
    ts = message.body
    #msg = ts.decode('utf8', 'ignore')
    #msg = ts.encode('utf8', 'ignore')
    self.safePrint("[" + ctime + "] (" + room.name + ") "+user.name + ': ' + message.body)
    try: #Try statement to prevent crashing over successfully sending certain characters.
	
     if message.body[0] == "!":     #Command prefix

      data = message.body[1:].split(" ", 1)

      if len(data) > 1:

        cmd, args = data[0], data[1]
	args = args.encode("utf8", "strict")

      else:

        cmd, args = data[0], " "

#start of commands



      if cmd == 'whoami':
       status = readAdmin(user.name)
       if status == True:
        room.message('Bot admin')
       else:
        room.message('A puny user :3')

      elif cmd == 'join':
       status = readAdmin(user.name)
       if status == True:
        self.joinRoom(args)
        logging.info("[" + curtime() + "] join command used by " + user.name + ", joined room " + args)

      elif cmd == 'part':
       status = readAdmin(user.name)
       if status == True:
        self.leaveRoom(args)
        logging.info("[" + curtime() + "] part command used by " + user.name + ", left room " + args)

#      elif cmd == "exec":
#       status = readAdmin(user.name)
#       if status == True:
#        try:
#         exec(args)
#        except:
#         room.message("Nothing")

      elif cmd == "eval":
       if readAdmin(user.name) == True:
        try:
         logging.info("[" + curtime() + "] eval command used by " + user.name + ", trying to eval " + args)
         room.message(eval(args))
        except Exception as err:
         room.message('<b>Err:</b> ' + str(err), True)
      elif cmd == 'say':
       global echo
       if echo == 0:
        room.message(args)
       elif echo == 1:
        if readAdmin(user.name) == True :
         room.message(args)
       elif echo == 2:
         print("!say is disabled.")

      elif cmd == 'quiet':		#Command that the bot wont respond to any users issuing a command
       status = readAdmin(user.name)
       if status == True:
        room.setSilent(True)
        quiet = 1
        logging.info("[" + curtime() + "] quiet command used by " + user.name + ", bot will no longer respond to general commands ")

      elif cmd == 'enable':
       status = readAdmin(user.name)
       if status == True:
        room.setSilent(False)
        quiet = 0
        logging.info("[" + curtime() + "] enable command used by " + user.name + ", bot will respond to all commands")

      elif cmd == 'hug':
       room.message('*hugs {user}*'.format(user=user.name))

      elif cmd == 'bestpony':
       poni = random.choice(open('bestpony.txt', 'r').readlines())
       room.message(poni)

      elif cmd == 'diabetes': # !pony probably makes this obsolete
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
        room.message(u1+" x... Never mind..")  #Selfcest, huehuehue
       else:
        room.message(u1+" x "+u2)

      elif cmd == 'calc':  #Remove old calc function
       room.message("This command is unsafe")

      elif cmd == 'shiny':
       shi = str(random.randint(1,65535))
       if shi <= 8:
        room.message('You got shiny!')
       else:
        room.message('Nope')


      elif cmd.startswith("goslate."):  #Currently not working due to unicode issues
       try:
        lang = cmd.split(".", 1)[1]
        trans = slate(args, lang).encode("utf-8").decode("utf-8")
        room.message(trans)
       except Exception as e:
        synmsg = "<b>Syntax</b>: !goslate.language Text here (where language is the abbreviation like 'ru')"
        room.message(synmsg, True)
        print(traceback.format_exc())

      elif cmd == "fontcolor":
       status = readAdmin(user.name)
       if status == True:
        try:
         self.setFontColor(args)
        except:
         room.message("Wrong")

      elif cmd == "setfont":
       status = readAdmin(user.name)
       if status == True:
        self.setFontColor(settings.fontcolor)
        self.setNameColor(settings.namecolor)
        self.setFontSize(settings.fontsize)
        room.message("Done")


      elif cmd == "restart":
       status = readAdmin(user.name)
       if status == True:
        room.message("Restarting..")
        pid = str(os.getpid())
        room.disconnect()
        os.system("./rstart.sh "+pid)

      elif cmd.startswith("echo."):
       global echo
       sw = cmd.split(".", 1)[1]
       status = readAdmin(user.name)
       if status == True:
        if sw == "on":
         echo = 0
         room.message("!say command is now usable by all users")
        elif sw == "botadmin":
         echo = 1
         room.message("!say command is now botadmin only")
        elif sw == "off":
         echo = 2
         room.message("!say command is disabled.")
        else:
         room.message("Switches are: on, botadmin, and off")

      elif cmd.startswith("derpi."):   #Derpibooru command
       sw = cmd.split(".", 1)[1]
       if sw == "info":
         room.message("The !derpi.* command is a function that gets the stats off a derpibooru image using JSON, the available commands are: !derpi.img <image num ID> (Note: !derpi.img needs a moment to grab the stats), !derpi.tag <tag name>")


       elif sw == "spoiler":
        s1 = str(args.replace(" ", "+"))
        s1 = str(s1.replace(":", "-colon-"))
        tagct = derpi.tagsp(args)
        if tagct is None:
          room.message("No spoiler image for tag <b>{args}</b>".format(args=args), True)
        else:
          room.message("Spoiler image for tag <b>{arg}</b>: {spoilerurl}".format(arg=args,spoilerurl=tagct), True)

      elif cmd == "fontsize":
       status = readAdmin(user.name)
       if status == True:
        try:
         self.setFontSize(args)
        except:
         room.message("Wrong")

      elif cmd == "namecolor":
       status = readAdmin(user.name)
       if status == True:
        try:
         self.setNameColor(args)
        except:
         room.message("Wrong")

      elif cmd == "reverse":
       rev = str(args[::-1])
       room.message(rev)


      elif cmd == "pony":
       rand = derpi.randcute()
       room.message("PONY PONY PONY https://derpiboo.ru/"+rand)


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

       elif sw == 'img':
        try:
         urllib2.urlopen("http://img.pokemondb.net/artwork/"+args+".jpg")
         psp = "http://img.pokemondb.net/artwork/"+args+".jpg"
         room.message(psp)
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
       if status == True:
        with open('quotes.txt', 'a') as qfile:
         qfile.write(args)
         room.message("Added quote ("+args+") to file.")

      elif cmd == "greetmsg":  #so many if/else statements
       status = readAdmin(user.name)
       if status == True:
        global greetmsg

        if args == "off":
          if greetmsg == False:
            room.message("It's already disabled")
          else:
            greetmsg = False
            room.message("Greet messages are now disabled")
        elif args == "on":
          if greetmsg == True:
            room.message("It's already enabled")
          else:
            greetmsg = True
            room.message("Greet messages are now enabled")
       else:
        room.message("Permission denied")

      elif cmd == "quote":
       qmsg = random.choice(open('quotes.txt', 'r').readlines())
       room.message(qmsg)

      elif cmd == "sauce":
       rstatus = readRoom(room.name)
       if rstatus == True:
        sauce = random.choice(open('sauce.txt', 'r').readlines())
        room.message(sauce)

      elif cmd == "lines":
       lct = str(len(open('pinchybot.py').readlines()))
       room.message("It takes {ln} lines to run PinchyBot!".format(ln=lct))

      elif cmd == "uptime":
       u = str(uptime())
       room.message("Uptime: "+u)

      elif cmd == "fpix":
       link = "http://fp.chatango.com/profileimg/%s/%s/%s/full.jpg" % (args[0], args[1], args)
       room.message(link)

      elif cmd.startswith("timer."):
       sw = cmd.split(".", 1)[1]
       if sw == 's':
        def ttimer( dur, u):
         count = 0
         while True:
          time.sleep(1)
          count += 1
          if count == dur:
           print("Timeup")
           room.message("Timeup for %s!" % (u))
           break
        try:
         if int(args) <= 0:
          room.message("Number needs to be higher than 0")
         elif int(args) > 172800:
          room.message("Upper limit is 172800")
         else:
          thread.start_new_thread(ttimer, (int(args), user.name ) )
          room.message("Timer started for %s seconds for %s" % (args, user.name))
          
        except:
         room.message("You did it wrong")

       elif sw == 'm':
        def ttimer( dur, u):
         count = 0
         while True:
          time.sleep(60)
          count += 1
          if count == dur:
           print("Timeup")
           room.message("Timeup for %s!" % (u))
           break
        try:
         if int(args) <= 0:
          room.message("Number needs to be higher than 0")
         elif int(args) > 2880:
          room.message("Upper limit is 2880")
         else:
          thread.start_new_thread(ttimer, (int(args), user.name ) )
          room.message("Timer started for %s minutes for %s" % (args, user.name))
          
        except:
         room.message("You did it wrong")

       elif sw == 'h':
        def ttimer( dur, u):
         count = 0
         while True:
          time.sleep(3600)
          count += 1
          if count == dur:
           print("Timeup")
           room.message("Timeup for %s!" % (u))
           break
        try:
         if int(args) <= 0:
          room.message("Number needs to be higher than 0")
         elif int(args) > 48:
          room.message("Upper limit is 48")
         else:
          thread.start_new_thread(ttimer, (int(args), user.name ) )
          room.message("Timer started for %s hours for %s" % (args, user.name))
          
        except:
         room.message("You did it wrong")



      elif cmd.startswith("help."):
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
        room.message("National Pokedex. This function links an image of the pokemon, plus the link to its info. The available commands are !dex.name <name of pokemon> (Exclude the brackets and do not use caps), !dex.img <name> (This goes for alternate forms such as Shaymin's Sky forme (shaymin-sky)", True)




      elif cmd == "tag":
       try:
        null = ['null']
        s1 = str(args.replace(" ", "+"))
        s1 = str(s1.replace(":", "-colon-"))
        tagct = derpi.tagsearch(args)
        searchlink = "http://derpiboo.ru/tags/"+s1
        msg = searchlink+" Tag <b>"+args+"</b> has "+tagct+" images"
        room.message(msg, True)
       except Exception as ee:
        emsg = "Tag <b>"+args+"</b>? That dosen't exist!"
        room.message(emsg, True)


      elif cmd == "wz":
       try:
        zzip = wzip(user.name)
        met = int(wmetric(user.name))
        msg = wz.wstring(zzip, met)
        room.message(msg, True)
       except Exception as e:
        print("nope ("+str(e)+")")
        room.message("I don't have your weather data stored, ask the owner if you want your data stored, otherwise use !wz.zip <zip code>")

      elif cmd == "wz.":
       sw = cmd.split(".", 1)[1]
       if sw == "zip":
        try:
         msg = wz.wstring(args, 0)
         room.message(msg, True)
        except:
         room.message("I need a zip code")

        

      elif cmd == 'metric':
       met = UserMetric(user.name)
       if met == 1:
        room.message("Your setting is currently set to Metric. Ask the bot owner if you want to change this setting.")
       else:
        room.message("Your setting is currently set to Imperial(Default setting), ask the bot owner if you want to change this setting.")

      elif cmd == "gimg":
       room.message(gimg.search(args))

      elif cmd == "tempconv.":
       sw = cmd.split(".", 1)[1]
       res = tempconv(sw, float(args))
       room.message(res)

      elif cmd == "cd":
       event = json.load(open("cd.json", "r"))
       if time.time() >= event['ts']:
        room.message("Time is already up")
       else:
	timeremain = str(timedelta(seconds=int(event['ts'] - time.time())))
        room.message("Time remaining for <b>{evname}</b> is: {tremain}".format(evname=event['EventName'],tremain=timeremain), True)

      elif cmd == "version":
       room.message("PinchyBot {ver}".format(ver=version_string))

       

#start of raw commands
     if message.body.startswith("the game"):
      dish = random.randint(1, 9)
      if dish == 3:
       room.message("SHUT UP YOU DISH")
      else:
       print("No.")

     if message.body.startswith("wat"):
      wat = random.randint(1, 20)
      if wat == 5:
       room.message("Wat.")
      else:
       print("No.")

     elif message.body.startswith("https://"):

      if message.body.startswith("https://derpibooru.org/"):
       try:
        num = message.body.split("g/", 1)[1]
        num = num.split("?")[0]
        msg = derpi.stats_string(num)
        room.message(msg, True)
       except Exception as e:
        print(traceback.format_exc)

      elif message.body.startswith("https://derpiboo.ru/"):
       try:
        num = message.body.split("u/", 1)[1]
        num = num.split("?")[0]  #This will strip anything starting with "?", this is to get rid of the 'scope' parameter on the URL before parsing
        msg = derpi.stats_string(num)
        room.message(msg, True)
       except:
        print("Derp")

      elif message.body.startswith("https://derpicdn.net/"):
       print("Derpi URL")

      elif message.body.startswith("https://www.youtube.com/"):
       try:
        vid = message.body.split("watch?v=", 1)[1]
        string = yt.stats_string(vid)
        room.message(string, True) 
       except:
        print("derp")

      elif message.body.startswith("https://img.pokemondb.net/artwork/"):
       ignoreurl()

      elif message.body.endswith(".jpg"):
       ignoreurl()

      elif message.body.endswith(".png"):
       ignoreurl()
      elif message.body.endswith(".gif"):
       ignoreurl()

      else:

       try:	#Any URLs that aren't ignored
        title = urlparse(message.body)
        room.message(title, True)
       except Exception as e:
        room.message("Dead URL?")
        print str(e)

     elif message.body.startswith("http://"):
      if message.body.startswith("http://derpibooru.org/"):  #Starting here is URLs the bot will ignore, this includes image URLs
       try:
        num = message.body.split("g/", 1)[1]
        num = num.split("?")[0]  #This will strip anything starting with "?", this is to get rid of the 'scope' parameter on the URL before parsing
        msg = derpi.stats_string(num)
        room.message(msg, True)
       except:
        print("Derp")

      elif message.body.startswith("http://derpiboo.ru/"):
       try:
        num = message.body.split("u/", 1)[1]
        num = num.split("?")[0]  #This will strip anything starting with "?", this is to get rid of the 'scope' parameter on the URL before parsing
        msg = derpi.stats_string(num)
        room.message(msg, True)
       except:
        print("Derp")

      elif message.body.startswith("http://derpicdn.net/"):
       ignoreurl()
      elif message.body.startswith("http://www.youtube.com/"):
       try:
        vid = message.body.split("watch?v=", 1)[1]
        string = yt.stats_string(vid)
        room.message(string, True) 
       except:
        print("derp")
      elif message.body.startswith("http://img.pokemondb.net/artwork/"):
       ignoreurl()
      elif message.body.endswith(".jpg"):
       ignoreurl()
      elif message.body.endswith(".png"):
       ignoreurl()
      elif message.body.endswith(".gif"):
       ignoreurl()
      else:
       try:
        title = urlparse(message.body)
        room.message(title, True)
       except Exception as e:
        room.message("Dead URL?")
        print str(e)
    except:
     print(traceback.format_exc())


       
#end of group chat commands

  def onFloodBan(self, room):   #This is why i set the bot's testing room to slow mode
    print("You are flood banned in "+room.name)

  def onPMMessage(self, pm, user, body):
    self.safePrint('['+curtime()+'] (PM) ' + user.name + ': ' + body) # '(PM) username: message string'
    if body[0] == "!":     #Command prefix

      data = body[1:].split(" ", 1)

      if len(data) > 1:

        cmd, args = data[0], data[1]

      else:

        cmd, args = data[0], " "

      #start of PM commands

      if cmd == "hi":
       pm.message(user, "Hai!")

      elif cmd == "info":
       pm.message(user, "I am a chatango bot coded in python, i was created by chaoticrift/crimsontail0 ( http://chaoticrift.chatango.com/ or http://crimsontail0.chatango.com/ ). The command list is here: http://pastebin.com/H3ktv6VT")

      elif cmd == "join":
       status = readAdmin(user.name)
       if status == True:
        self.joinRoom(args)
        pm.message(user, "Joined "+args)
       else:
        pm.message(user, "Permission denied")

      elif cmd == "part":
       status = readAdmin(user.name)
       if status == True:
        self.leaveRoom(args)
        pm.message(user, "Left "+args)
       else:
        pm.message(user, "Permission denied")

      elif cmd == "pony":
       rand = derpi.randcute()
       pm.message(user, "PONY PONY PONY http://derpiboo.ru/"+rand)

      elif cmd == "lines":
       lct = str(len(open('pinchybot.py').readlines()))
       pm.message(user, "It takes "+lct+" lines to run PinchyBot!")

      elif cmd == '8ball':
       rand = ['Yes', 'No', 'Outlook so so', 'Absolutely', 'My sources say no', 'Yes definitely', 'Very doubtful', 'Most likely', 'Forget about it', 'Are you kidding?', 'Go for it', 'Not now', 'Looking good', 'Who knows', 'A definite yes', 'You will have to wait', 'Yes, in my due time', 'I have my doubts']
       pm.message(user, random.choice(rand))

      elif cmd == 'bestpony':
       poni = bestpone()
       pm.message(user, poni)

      elif cmd == 'ping':
       pm.message(user, 'Pong')

      elif cmd == 'uptime':
       u = str(uptime())
       pm.message(user, "Uptime: "+u)

      elif cmd == "eval":
       status = readAdmin(user.name)
       if status == True:
        try:
         logging.info("[" + curtime() + "] eval command used by " + user.name + ", trying to eval " + args)
         pm.message(user, eval(args))
        except Exception as err:
         pm.message(user, 'Err: ' + str(err))
       else:
         pm.message(user, "Permission denied")


if __name__ == "__main__":  #Multiple rooms separated by commas(each must be covered in quotation marks)
  PinchyBot.easy_start(settings.rooms, settings.nickname, settings.nickpass)
