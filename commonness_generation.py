#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
disamb_freq_map = {}

def add_link(term):
    main_term = remove_last_parentheses(term)
    if main_term in disamb_freq_map:
        ind_list = disamb_freq_map[main_term]
        if term in ind_list:
            disamb_freq_map[main_term][term] += 1
        else:
            disamb_freq_map[main_term][term] = 1
    else:
        disamb_freq_map[main_term] = {}
        disamb_freq_map[main_term][term] = 1

def remove_last_parentheses(term):
    if term[-1] == ')':
        index = term.rfind('(')
        term = term[:index]
    return term.strip(' _')
    

def count_terms(links):
    for l in links:
        l = l.split('|')[0]
        if good_term(l):
            add_link(l) 
def good_term(link):
    if link.find('Image:') == 0:
        return False
    return True

for fn in glob.glob('500MB_*.xml'):
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    for child in root.findall('.//{0}text'.format(namespace)):
        content = child.text
        links = re.findall('\[\[(.*?)\]\]', content)
        count_terms(links)

for main_term in disamb_freq_map:
    term_list = disamb_freq_map[main_term]
    term_count = 0
    for term in term_list:
        term_count += term_list[term]
    for term in term_list:
        term_list[term] /= float(term_count)

freq_map = {}
for main_term in disamb_freq_map:
    for term in disamb_freq_map[main_term]:
        freq_map[term] = disamb_freq_map[main_term][term]
    
json.dumps(freq_map)
with open(os.path.basename('freq_map_'+str(int(time.time())) + '.xml'), 'wb') as local_file:
    local_file.write(json.dumps(freq_map))
