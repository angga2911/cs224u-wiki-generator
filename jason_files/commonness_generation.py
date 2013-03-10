#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree
from 

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"
disamb_freq_map = {}

source_dir = 'TEST'
out_dir = 'COMMONNESS_MEAS'
def add_link(term):
    if len(term) == 0:
        return
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
    if len(term) != 0 and term[-1] == ')':
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
    
abs_dir_output = os.path.join(h(), out_dir, 'CMN_'+str(int(time.time())) + '.xml')
with open(os.path.abspath(abs_dir_output), 'wb') as local_file:
    local_file.write(json.dumps(freq_map))
