#!/usr/bin/env python2

import ircbot
import re
import sys
import random
import urlparse
import urllib2
from bs4 import BeautifulSoup

server = sys.argv[1]
channel = sys.argv[2]

class yay(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(server, 6667)], "yay", "yet another yppy")

    def on_welcome(self, serv, ev):
        serv.join(channel)

    def on_pubmsg(self, serv, ev):
        canal = ev.target()
        message = ev.arguments()[0].lower()
        if self.channels[canal].has_user("Yppy"):
            return
        url = re.search("(?P<url>https?://[^\s]+)", message)
        if url:
            url = url.group(0)
            hostname = urlparse.urlparse(url).hostname
            try:
                tinyurl = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url).read()
                soup = BeautifulSoup(urllib2.urlopen(url))
                ret = "Title : %s (%s) | %s" % (soup.title.string[:50], hostname, tinyurl)
                serv.privmsg(canal, ret)
            except IOError:
                return

if __name__ == "__main__":
    yay().start()