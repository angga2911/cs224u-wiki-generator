#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib, urllib2, os, time, webbrowser
from urllib2 import urlopen, Request, URLError, HTTPError

random_article = 'http://en.wikipedia.org/wiki/Special:Random'
dumper = 'http://en.wikipedia.org/w/index.php?title=Special:Export&action=submit'

terms = []
for i in range(2):
  usock = urllib2.Request(random_article, headers={"User-Agent" : "Magic Browser"})
  data = urllib2.urlopen(usock)
  #print data.geturl().rsplit('/', 1)[1]
  terms.append(data.geturl().rsplit('/', 1)[1]) 
  #wiki_page = BeautifulSoup(data.read())
input_to_dump = "%0A".join(terms)
print input_to_dump
try:
  usock = urllib2.Request(dumper+"&pages="+input_to_dump, headers={"User-Agent" : "Magic Browser"})
  f = urlopen(usock)
  print 'downloading ' + dumper+"&pages="+input_to_dump

  with open(os.path.basename(str(int(time.time())) + '.xml'), 'wb') as local_file:
    local_file.write(f.read())

except HTTPError, e:
  print "HTTP Error:", e.code, input_to_dump
except URLError, e:
  print "URL Error:", e.reason, input_to_dump

