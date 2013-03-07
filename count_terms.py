#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
freq_map = {}

def add_link(term):
    if term in freq_map:
        freq_map[term] += 1
    else:
        freq_map[term] = 1

def count_terms(links):
    for l in links:
        add_link(l) 

for fn in glob.glob('500MB_*.xml'):
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    for child in root.findall('.//{0}text'.format(namespace)):
        content = child.text
        links = re.findall('\[\[(.*?)\]\]', content)
        count_terms(links)

json.dumps(freq_map)
with open(os.path.basename('freq_map_'+str(int(time.time())) + '.xml'), 'wb') as local_file:
    local_file.write(json.dumps(freq_map))
