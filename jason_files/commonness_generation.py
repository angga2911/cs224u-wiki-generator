#!/usr/bin/python

import glob, re, json, os, time
import xml.etree.cElementTree as etree
from jason_files import disambiguate
from multiprocessing import Pool

namespace = "{http://www.mediawiki.org/xml/export-0.8/}"

source_dir = '500MB_FILES'
out_dir = 'COMMONNESS_MEAS'
disam_freq_map = {}
def add_link(term):
    disam_freq_map_ind = {}
    if len(term) == 0 or not good_term(term):
        return
    main_term = remove_last_parentheses(term).replace(' ', '_')
    if main_term not in disam_freq_map_ind:
        disam_freq_map_ind[main_term] = {}
        disam_list = disambiguate.disambiguate(main_term)
        for term in disam_list:
            disam_freq_map_ind[main_term][term] = 0
    return disam_freq_map_ind

def good_term(link):
    if link.find('Image:') == 0:
        return False
    if link.find('File:') == 0:
        return False
    if link.find('Category:') == 0:
        return False
    return True

def count_link(term):
    if len(term) == 0:
        return
    for main_term in disam_freq_map:
        term_dict = disam_freq_map[main_term]
        if term in term_dict:
            disam_freq_map[main_term][term] += 1
            
def remove_last_parentheses(term):
    if len(term) != 0 and term[-1] == ')':
        index = term.rfind('(')
        term = term[:index]
    return term.strip(' _')

def chunks(l, n):
    return [l[i:i+n] for i in range(0, len(l), n)]    

pool = Pool(processes=100)
def find_terms(links):
    global disam_freq_map
    links = [l.split('|')[0] for l in links]
    chunked = chunks(links, 4000)
    for l in chunked:
        each_freq_map = pool.map(add_link, l)
        for ind_dict in each_freq_map:
            if ind_dict != None:
                disam_freq_map = dict(disam_freq_map.items()+ind_dict.items())

def count_terms(links):
    links = [l.split('|')[0] for l in links]
    for l in links:
        if good_term(l):
            count_link(l) 

def h():
    return os.path.abspath(os.path.dirname(__file__))

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

abs_dir_input = os.path.join(source_dir, '500MB_*.xml')
# Create list of disambiguations
chunk = 1
for fn in glob.glob(abs_dir_input):
    print "Process Chunk: " + str(chunk) + "/" + str(len(glob.glob(abs_dir_input)))
    chunk = chunk + 1
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    links = []
    for child in root.findall('.//{0}text'.format(namespace)):
        content = child.text
        links.extend(re.findall('\[\[(.*?)\]\]', content))
    find_terms(links)

# Count disambiguations
for fn in glob.glob(abs_dir_input):
    f = open(fn, 'r')
    xml = f.read()
    root = etree.fromstring(xml)
    links = []
    for child in root.findall('.//{0}text'.format(namespace)):
        content = child.text
        links = re.findall('\[\[(.*?)\]\]', content)
        count_terms(links)

for main_term in disam_freq_map:
    term_list = disam_freq_map[main_term]
    term_count = 0
    for term in term_list:
        term_count += disam_freq_map[main_term][term]
    for term in term_list:
        if term_count != 0:
            disam_freq_map[main_term][term] /= float(term_count)
        else:
            disam_freq_map[main_term][term] = 0

freq_map = {}
for main_term in disam_freq_map:
    for term in disam_freq_map[main_term]:
        freq_map[term] = disam_freq_map[main_term][term]
    
abs_dir_output = os.path.join(h(), out_dir, 'CMN_'+str(int(time.time())) + '.xml')
with open(os.path.abspath(abs_dir_output), 'wb') as local_file:
    local_file.write(json.dumps(freq_map))
