import os
import re
import shutil
from tqdm import tqdm
import ptree

# def extract_xml_links(input_file, output_file, rx_keep, rx_ignore):
def extract_all_links(bibcode, all_links_file):
    ''' given a path to all.links file that holds info about source
    extracts a bibcodes and matching link matching
    bibcode: bibcode to extract links for
    all_links_file: path to all.links file'
    '''
    # if os.path.exists(output_file):
    #     raise ValueError('file already exists, exiting.')

    # open links file
    with open(all_links_file, 'r') as f:
        links = f.read().splitlines()
        
    
    # Search for bibcodes in the links file
    # bibcodes = ['2019A&A...623A..72G', '2019A&A...623A..72G']
    # link = [l for l in links if any([b in l for b in bibcodes])]
    print(f'all.links open, searching for {bibcode}')
    # import pdb;pdb.set_trace()
    # matches = []
    # for match in links:
    #     if bibcode in match:
    #         matches.append(match)
    link = [l for l in links if bibcode in l]
    print(link)
    # import pdb;pdb.set_trace()
    # link = [l for l in links if bibcode in links]
    
    # Replace '\t' with ' ' in the links
    # link = link.replace('\t', ' ')

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

