#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"

link_map = {}
source_dir = '500MB_FILES'
out_dir = 'INCOMING_LINKS'

def add_link(title, link):
    if link in link_map:
        link_map[link].append(title)
    else:
        link_map[link] = [title]

def h():
    return os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(source_dir):
    os.makedirs(source_dir)

abs_dir_input = os.path.join(source_dir, '500MB_*.xml')
for fn in glob.glob(abs_dir_input):
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

abs_dir_output = os.path.join(h(), out_dir, 'IL_'+str(int(time.time())) + '.xml')
with open(os.path.abspath(abs_dir_output), 'wb') as local_file:
    local_file.write(json.dumps(link_map))
