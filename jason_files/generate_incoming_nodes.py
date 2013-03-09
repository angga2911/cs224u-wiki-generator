#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"

link_map = {}
def add_link(title, link):
    if link in link_map:
        link_map[link].append(title)
    else:
        link_map[link] = [title]

for fn in glob.glob('500MB_*.xml'):
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    for page in root.findall('.//{0}page'.format(namespace)):
        title = [w.text for w in page.findall('.//{0}title'.format(namespace))]
        title = [w.replace(' ', '_') for w in title]
        text = [w.text for w in page.findall('.//{0}text'.format(namespace))]
        for ttl in title:
            for txt in text:
                for link in re.findall('\[\[(.*?)\]\]', txt):
                    add_link(ttl, link)

with open(os.path.basename('incoming_links_'+str(int(time.time())) + '.xml'), 'wb') as local_file:
    local_file.write(json.dumps(link_map))
