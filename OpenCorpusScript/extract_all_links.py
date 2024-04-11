import os
import re
import shutil
from tqdm import tqdm
import ptree

def extract_all_links(bibcode, all_links_file):
    ''' given a path to all.links file that holds info about source
    extracts a bibcodes and matching link matching
    bibcode: bibcode to extract links for
    all_links_file: path to all.links file'
    '''

    with open(all_links_file, 'r') as f:
        links = f.read().splitlines()
    
    # Search for bibcodes in the links file
    print(f'Searching all.links for {bibcode}')
    link = [l for l in links if bibcode in l]
    print(link)
    

    try:
        link = link[0]
        splitline = link.split('\t')
        source_bibcode = splitline[0]
        source_path = splitline[1]

        source_filename = source_path.split('/')[-1]
             
        source_dict = {'source_bibcode' : source_bibcode,
                       'source_path' : source_path,
                       'source_filename' : source_filename}
    except:
        source_dict = None

    return source_dict

