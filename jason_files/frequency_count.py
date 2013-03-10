#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree

freq_map = {}
namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
source_dir = '500MB_FILES'
out_dir = 'FREQ_MAP'

def add_link(term):
    if term in freq_map:
        freq_map[term] += 1
    else:
        freq_map[term] = 1

def count_terms(links):
    for l in links:
        add_link(l) 

def h():
    return os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

abs_dir_input = os.path.join(source_dir, '500MB_*.xml')
for fn in glob.glob(abs_dir_input):
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    for child in root.findall('.//{0}text'.format(namespace)):
        content = child.text
        links = re.findall('\[\[(.*?)\]\]', content)
        count_terms(links)

abs_dir_output = os.path.join(h(), out_dir, 'freq_map_'+str(int(time.time())) + '.xml')
with open(os.path.abspath(abs_dir_output), 'wb') as local_file:
    local_file.write(json.dumps(freq_map))
