import urllib2
import json
import decimal

#To grab video stats off a youtube video using JSON


def title(vid):    #Get title
    url = urllib2.urlopen('https://gdata.youtube.com/feeds/api/videos/'+vid+'?v=2&alt=json')
    jso = json.load(url)
    lst = jso['entry']['title']['$t']
    return str(lst)


def length(vid):    #Get video length in seconds
    url = urllib2.urlopen('https://gdata.youtube.com/feeds/api/videos/'+vid+'?v=2&alt=json')
    jso = json.load(url)
    lst = jso['entry']['media$group']['yt$duration']['seconds']
    return int(lst)

def views(vid):    #Get views
    url = urllib2.urlopen('https://gdata.youtube.com/feeds/api/videos/'+vid+'?v=2&alt=json')
    jso = json.load(url)
    lst = jso['entry']['yt$statistics']['viewCount']
    return str(lst)



def time(sec):   #This converts the seconds to a timestamp. Eg: 900 changes to 15:00
    hr = eval(str(sec / 3600))
    mi = eval(str(sec / 60))
    se = eval(str(mi * 60))
    fin = eval(str(sec - se))
    fmh = eval(str(hr * 60))
    fmi = eval(str(mi - fmh))
    if hr > 0:
     if fmi < 10 and fin < 10:
      return str(str(hr)+":0"+str(fmi)+":0"+str(fin))
     elif fmi < 10:
      return str(str(hr)+":0"+str(fmi)+":"+str(fin))
     elif fin < 10:
      return str(str(hr)+":"+str(fmi)+":0"+str(fin))
     else:
      return str(str(hr)+":"+str(fmi)+":"+str(fin))



    elif mi < 10 and fin < 10:
     return str("0"+str(mi)+":0"+str(fin))
    elif fin < 10:
     return str(str(mi)+":0"+str(fin))
    elif min < 10:
     return str("0"+str(mi)+":"+str(fin))
    else:
     return str(str(mi)+":"+str(fin))


def rateu(vid):   #Get the upvotes
    url = urllib2.urlopen('https://gdata.youtube.com/feeds/api/videos/'+vid+'?v=2&alt=json')
    jso = json.load(url)
    upv = jso['entry']['yt$rating']['numLikes']
    return str(upv)

def rated(vid):  #Get the downvotes
    url = urllib2.urlopen('https://gdata.youtube.com/feeds/api/videos/'+vid+'?v=2&alt=json')
    jso = json.load(url)
    dowv = jso['entry']['yt$rating']['numDislikes']
    return str(dowv)

def vstat(vid):   #something useless
    ti = title(vid)
    ln = length(vid)
    vi = views(vid)
    tim = time(ln)
    res = "Youtube video: "+ti+" | Length: "+tim+" | Views: "+vi
