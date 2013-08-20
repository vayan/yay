#!/usr/bin/env python2

import ircbot
import re
import sys
import urlparse
import urllib2
import unirest
from goose import Goose

server = sys.argv[1]
channel = sys.argv[2]

class yay(ircbot.SingleServerIRCBot):
    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [(server, 6667)], "yay", "yet another yppy")
        self.lastur = "https://www.google.com"

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
            try:
                self.lasturl = url
                hostname = urlparse.urlparse(url).hostname
                g = Goose()
                article = g.extract(url=url)
                tinyurl = urllib2.urlopen("http://tinyurl.com/api-create.php?url=" + url).read()
                title = article.title.encode('utf-8')[:70]
                ret = "Title : %s (%s) | %s" % (title, hostname, tinyurl)
                serv.privmsg(canal, ret)
            except:  # todo log error
                e = sys.exc_info()[0]
                print(e)
                return
        if "!sum" in message:
            try:
                response = unirest.post("http://192.81.222.194:1142/api",{}, {"url": self.lasturl})
                print response.body
                for bullet in response.body:
                    serv.privmsg(canal, ("* %s" % (bullet).encode('utf-8')))
            except:  # todo log error
                e = sys.exc_info()[0]
                print(e)
                return

if __name__ == "__main__":
    yay().start()
