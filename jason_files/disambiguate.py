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
      to_return = [w for w in to_return if levenshtein(w,keyword) <0.6]
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
  
def levenshtein(s1, s2):
  l1 = len(s1)
  l2 = len(s2)

  matrix = [range(l1 + 1)] * (l2 + 1)
  for zz in range(l2 + 1):
    matrix[zz] = range(zz,zz + l1 + 1)
  for zz in range(0,l2):
    for sz in range(0,l1):
      if s1[sz] == s2[zz]:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz])
      else:
        matrix[zz+1][sz+1] = min(matrix[zz+1][sz] + 1, matrix[zz][sz+1] + 1, matrix[zz][sz] + 1)
  return matrix[l2][l1]/float(max(l1,l2))

#print disambiguate('Michael_Jordan') 
#print get_article_links(disambiguate('Cube'))
#print get_article_links(disambiguate('Andrew_Ng'))
#print disambiguate('Andrew_Ng')
#print disambiguate('Lexicon')
#print disambiguate('State')
#print disambiguate('Legion')
#print disambiguate('Tell')
#print disambiguate('Well')

