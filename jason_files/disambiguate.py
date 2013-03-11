#! /usr/bin/python

from bs4 import BeautifulSoup
from HTMLParser import HTMLParseError
import urllib, urllib2, os, time, webbrowser, re
from urllib2 import urlopen, Request, URLError, HTTPError

wikipedia = 'http://en.wikipedia.org/wiki/'

tries = 4
timeout = 1
def disambiguate(keyword):
  to_return = []
  for i in range(tries):
    try:
      to_test = keyword + '_(disambiguation)'
      usock = urllib2.Request((wikipedia+to_test).encode('utf-8'), headers={"User-Agent" : "Magic Browser"})
      response = urllib2.urlopen(usock)
      html = response.read()
      wiki_page = BeautifulSoup(html)
      ulist = wiki_page.find(id='mw-content-text')
      if ulist != None:
        primary_tag = ulist.p
        if primary_tag != None:
          primary_link = primary_tag.a
          if primary_link != None:
            primary_link = primary_link['href'].rsplit('/',1)
            if len(primary_link) > 1:
              primary_link = primary_link[1]
              if primary_link != None:
                to_return.append(primary_link)
        for ulchild in ulist.findAll('ul'):
          for lichild in ulchild.findAll('li'):
           for link in lichild.findAll('a'):
              if len(link['href'])>1 and link['href'][0] != '#' and not 'disambiguation' in link['href']:
                lnk = link['href'].rsplit('/', 1)
                if len(lnk) > 1:
                  lnk = lnk[1]
                  if lnk != None:
                    to_return.append(lnk)
      return to_return
    except HTMLParseError, e:
      return [keyword]
    except HTTPError, e:
      return [keyword]
    except URLError as e:
      continue


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

