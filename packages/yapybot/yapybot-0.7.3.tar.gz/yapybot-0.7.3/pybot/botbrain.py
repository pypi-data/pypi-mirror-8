from collections import defaultdict
import webwriter
import time
import logger 
import datetime
import urllib2
import json
from urlparse import urlparse, parse_qsl
import re
from xml.dom.minidom import parseString
#import db
from datetime import datetime, timedelta
import sys
import os
import lite

class BotBrain:
  BRAINDEBUG = False
  
  def __init__(self, microphone, bot=None):             
# get time for uptime start
    self.starttime = time.time()
# get time for current length of uptime
    self.localtime = time.localtime()
# get handle on output

    self.microphone = microphone
    self.bot = bot
    yth = dict()
    self.db = self.bot.db
    self.ww = webwriter.WebWriter()

  def _isAdmin(self, username):
    if self.bot.conf.getOwner(self.bot.network) == username:
      return True
    if self.db._isAdmin(username):
      return True
    return False

  def getMicrophone(self):
    return self.microphone

  def _updateSeen(self, user, statement, event):
    self.db.updateSeen(user, statement, event)
  
  def _insertImg(self, user, url, channel):
    self.db._insertImg(user, url, channel)

  def __bareSay(self, thing):
    self.microphone(thing + '\n')

  def say(self, channel, thing):
    try:
      s = thing.encode('utf-8', 'ignore')
    except UnicodeEncodeError as e:
      print e
      print thing
      return None
    except UnicodeDecodeError as d:
      print d
      print thing
      return None

    outstring = 'PRIVMSG ' + channel + ' :' + s.decode('utf-8','ignore') + '\n'
    self.microphone(outstring)

  def notice(self, channel, thing):
    self.microphone('NOTICE ' + channel + ' :' + str(thing) + '\n')

  # now implemented as a module
  #def _weather(self, channel, zipcode):

  # now implemented as a module
 # def _getyoutubetitle(self, line, channel):

  def _ctof(self, channel, c_temp):
    c = float(c_temp)
    f = (c * 1.8)+32
    self.say(channel, str(f) + "* F")

  def _ftoc(self, channel, f_temp):
    f = float(f_temp)
    c = (f - 32)*(.5555)
    self.say(channel, str(c) + "* C")

  def _uptime(self, channel):
    self.say(channel,"I've been up " +str(timedelta(seconds=time.time() - self.starttime))[:7] + ", since "+time.strftime("%a, %d %b %Y %H:%M:%S -0800", self.localtime))

  def _speak(self, user, target, message):
    if target.startswith("#"):
      self.say(target, message) 
    else:
      target = "#" + target
      self.say(target, message)

  def _onstat(self, channel):
    self.say(channel, "Yep, I'm on. Idiot.")

  def _help(self, user):
    self.microphone('PRIVMSG ' + user + ' :' + ".uptime,\n")
    self.microphone('PRIVMSG ' + user + ' :' + ".imgs,\n")
    self.microphone('PRIVMSG ' + user + ' :' + ".ctof [celsius],\n")
    self.microphone('PRIVMSG ' + user + ' :' + ".ftoc [fahrenheit],\n")

  def _join(self, usr, message):
    if self._isAdmin(usr):
      if len(message.split()) is 3:
        channel = message.split()[1]
        extraArg = message.split()[-1]
        self.__bareSay("JOIN " + channel + " " + extraArg)
      else:
        channel = message.split()[-1] # second word (join #channel password)
        self.__bareSay("JOIN " + channel)


  def __quit(self, usr):
    if self._isAdmin(usr):
      self.__bareSay("QUIT :quitting")
      print "quitting as per " + usr
      sys.exit()

  
  def respond(self, usr, channel, message):
# this bit is not a command
    if (".png" in message or ".gif" in message or ".jpg" in message or ".jpeg" in message) and ("http:" in message or "https:" in message) or ("imgur.com" in message and "gallery" in message):
     url = re.search("(?P<url>https?://[^\s]+)", message).group("url")
     if url:
       self._insertImg(usr, url, channel)
# this bit is
    if message.startswith(".join"):
      self._join(usr, message)
    if message.strip() == ".quit":
      self.__quit(usr)
    if message.startswith(".imgs"):
      self.ww._generate(self.db._getImgs())
      # hackish TODO
      if os.getenv('USER') == 'pybot':
        self.say(channel, "http://pybot.zero9f9.com/img/")
      else:
        self.say(channel, "http://zero9f9.com/~"+os.getenv('USER')+"/img/")
    #if message.startswith(".seen"):
    #  self._seen(message.split()[-1], channel)
    if message.startswith(".ctof"):
      last = message.split()
      if last[-1] != "":
        self._ctof(channel, last[-1])
    if message.startswith(".ftoc"):
      last = message.split()
      if last[-1] != "":
        self._ftoc(channel, last[-1]) 
    if message.startswith(".help"):
      self._help(usr)     
    if message.startswith(".onstat"):
      self._onstat(channel)
    if message.startswith(".speak"):
      tmp = message.split(" ",2)
      chnl = tmp[1]
      msg = tmp[2]
      self._speak(usr, chnl, msg)
