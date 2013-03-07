#! /usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib, urllib2, os, time, webbrowser, threading
from urllib2 import urlopen, Request, URLError, HTTPError
from multiprocessing import Pool
import Queue

random_article = 'http://en.wikipedia.org/wiki/Special:Random'
dumper = 'http://en.wikipedia.org/w/index.php?title=Special:Export&action=submit'

num_articles = 100

def get_redirected_url(url):
    opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
    opener.addheaders = [('User-Agent', 'Magic Browser')]
    request = opener.open(url)
    return request.url

def get_clean_term(r):
    try:
        term = 'List_of'
        while term.find('List_of') == 0:
            term = get_redirected_url(random_article).rsplit('/', 1)[1] 
        return term
    except HTTPError, e:
        return ''
    except URLError, e:
        return ''

pool = Pool(processes = 100)
terms = pool.map(get_clean_term, range(num_articles));
input_to_dump = "%0A".join(terms)
print input_to_dump

try:
    usock = urllib2.Request(dumper+"&pages="+input_to_dump, headers={"User-Agent" : "Magic Browser"})
    f = urlopen(usock)
    print 'downloading ' + dumper+"&pages="+input_to_dump

    with open(os.path.basename('500MB_'+str(int(time.time())) + '.xml'), 'wb') as local_file:
        local_file.write(f.read())

except HTTPError, e:
    print "HTTP Error:", e.code, input_to_dump
except URLError, e:
    print "URL Error:", e.reason, input_to_dump
