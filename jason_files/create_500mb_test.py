#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib, urllib2, os, time, webbrowser, threading
from urllib2 import urlopen, Request, URLError, HTTPError
from multiprocessing import Pool

num_articles = 50000
directory = '500MB_FILES'
random_article = 'http://en.wikipedia.org/wiki/Special:Random'
dumper = 'http://en.wikipedia.org/w/index.php?title=Special:Export&action=submit'

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
def fetch_hundred_pages():
    increment = 100
    terms = pool.map(get_clean_term, range(increment));
    input_to_dump = "%0A".join(terms)

    try:
        usock = urllib2.Request(dumper+"&pages="+input_to_dump, headers={"User-Agent" : "Magic Browser"})
        f = urlopen(usock)
        print 'downloading ' + dumper+"&pages="+input_to_dump

        abs_dir = os.path.join(h(), directory, '500MB_'+str(int(time.time())) + '.xml')
        with open(os.path.abspath(abs_dir), 'wb') as local_file:
            local_file.write(f.read())

    except HTTPError, e:
        print "HTTP Error:", e.code, input_to_dump
        return 0
    except URLError, e:
        print "URL Error:", e.reason, input_to_dump
        return 0
    return 100

def h():
    return os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(directory):
    os.makedirs(directory)

total = 0
while total < num_articles:
    total += fetch_hundred_pages()

print "Finished fetch 50,000 articles!"
