#! /usr/bin/python

from bs4 import BeautifulSoup
import urllib, urllib2, os, time, webbrowser, re
from urllib2 import urlopen, Request, URLError, HTTPError

wikipedia = 'http://en.wikipedia.org/wiki/'

def disambiguate(keyword):
  to_return = []
  try:
    to_test = keyword + '_(disambiguation)'
    usock = urllib2.Request(wikipedia+to_test, headers={"User-Agent" : "Magic Browser"})
    response = urllib2.urlopen(usock)
    html = response.read()
    wiki_page = BeautifulSoup(html)
    
    ulist = wiki_page.find(id='mw-content-text')
    primary_tag = ulist.p
    if primary_tag != None:
      primary_link = primary_tag.a
      if primary_link != None:
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

dumper = 'http://en.wikipedia.org/w/index.php?title=Special:Export&action=submit'
def get_article_links(links):
  input_to_dump = "%0A".join(links)
  try:
    usock = urllib2.Request(dumper+"&pages="+input_to_dump, headers={"User-Agent" : "Magic Browser"})
    f = urlopen(usock)
    #print 'downloading ' + dumper+"&pages="+input_to_dump

    text = f.read()
    link_result = re.findall('\[\[(.*?)\]\]', text)
    return link_result
  except HTTPError, e:
    print "HTTP Error:", e.code, input_to_dump
  except URLError, e:
    print "URL Error:", e.reason, input_to_dump
  return []
  

#print get_article_links(disambiguate('Michael_Jordan'))
#print get_article_links(disambiguate('Cube'))
#print get_article_links(disambiguate('Andrew_Ng'))
#print disambiguate('Andrew_Ng')
#print disambiguate('Lexicon')
#print disambiguate('State')
#print disambiguate('Legion')
#print disambiguate('Tell')
#print disambiguate('Well')

