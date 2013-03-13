#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib
import urllib2
import os
import time
from urllib2 import urlopen, Request, URLError, HTTPError
import webbrowser
import re

random_article = 'http://en.wikipedia.org/wiki/Special:Random'
dumper = 'http://en.wikipedia.org/w/index.php?title=Special:Export&action=submit'

def isAlpha(s, search=re.compile(r'[^a-zA-Z0-9. _(),]').search):
    #Note period, space, parenthese, and underscore are allowed.
    return not bool(search(s))

def invalidURL(s):
    shift = len("http://en.wikipedia.org/wiki/")
    sn =  s[shift:]
    if not isAlpha(sn):
        #print sn
        return True
    if sn.find('List_of') != -1:
        #print sn
        return True
    if sn.find('(disambiguation)') != -1:
        #print sn
        return True
    return False
    
j = 0
TARGET = 10
while j < TARGET:
    terms = []
    for i in range(100):
        #print data.geturl().rsplit('/', 1)[1]
        temp = 'http://en.wikipedia.org/wiki/List_of'
        while invalidURL(temp):
            usock = urllib2.Request(random_article, headers={"User-Agent" : "Magic Browser"})
            data = urllib2.urlopen(usock)
            temp = data.geturl()
        terms.append(temp.rsplit('/', 1)[1]) 
	    #wiki_page = BeautifulSoup(data.read())
        input_to_dump = "%0A".join(terms)
	   
    try:
        usock = urllib2.Request(dumper+"&pages="+input_to_dump, headers={"User-Agent" : "Magic Browser"})
        f = urlopen(usock)
        print 'downloading ' + dumper+"&pages="+input_to_dump

       
        with open('TRAINING/' + str(int(time.time())) + '.xml', 'wb') as local_file:
       # print f.read()
            pages = re.findall('<page>(.*?)</page>', f.read(), re.S)
            for page in pages:
           # links is a list of the hyperlinks
                links = re.findall('\[\[([^:]*?)\]\]', page)
               # print links
               # print len(links)
                set_links = set(links)
               # print set_links
               # print len(set_links)
               # print "-----------"
                if len(set_links) > 50: 
                    j = j + 1
                    #local_file.write("Article #" + str(j))
                    local_file.write("<page>\n")
                    local_file.write(page)
                    local_file.write("</page>\n")
                    #local_file.write("-------------------------------------------------\n")
    except HTTPError, e:
        print "HTTP Error:", e.code, input_to_dump
    except URLError, e:
        print "URL Error:", e.reason, input_to_dump
