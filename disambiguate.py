#! /usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib
import urllib2
import os
import time
from urllib2 import urlopen, Request, URLError, HTTPError
import webbrowser

wikipedia = 'http://en.wikipedia.org/wiki/'

def disambiguate(keyword):
  to_return = []
  try:
    to_test = keyword + '_(disambiguation)'
    print wikipedia + to_test
    usock = urllib2.Request(wikipedia+to_test, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(usock)
    html = response.read()
    wiki_page = BeautifulSoup(html)
    
    ulist = wiki_page.find(id='mw-content-text')
    primary_link = ulist.p.a
    primary_link = primary_link['href'].rsplit('/', 1)[1]
    if primary_link != None:
      to_return.append(primary_link)
    for ulchild in ulist.findAll('ul'):
      for lichild in ulchild.findAll('li'):
        for link in lichild.findAll('a'):
          if link['href'][0] != '#' and not 'disambiguation' in link['href']:
            lnk = link['href'].rsplit('/', 1)[1]
            if lnk != None:
              to_return.append(lnk)
    return to_return
  except HTTPError, e:
    return [keyword]
  except URLError, e:
    return [keyword]

  

print disambiguate('Michael_Jordan')
print disambiguate('Cube')
print disambiguate('Andrew_Ng')


