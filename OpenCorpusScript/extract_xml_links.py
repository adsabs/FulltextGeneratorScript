import os
import re
from tqdm import tqdm

# def extract_xml_links(input_file, output_file, rx_keep, rx_ignore):
def extract_xml_links(bibcodes, all_links_file, rx_keep='.*xml.*', rx_ignore='.*ocr'):
    ''' given a path to all.links file that holds info about fulltext,
    extracts a set of bibcodes and xml links matching the two regular expressions
    Saves the set as a txt file. No logging, no error checking.
    example regexs: -k '(19[5-9][0-9]|2[0-9]{3}).*\.xml' -g '.*ocr' 
    bibcodes: list of bibcodes to extract links for
    all_links_file: path to all.links file'
    rx_keep: only save bibcodes from lines that pass this regex filter
    rx_ignore: ignore lines that pass this regex filter
    '''
    # if os.path.exists(output_file):
    #     raise ValueError('file already exists, exiting.')

    # open links file
    with open(all_links_file, 'r') as f:
        links = f.read().splitlines()
        
    
    # Search for bibcodes in the links file
    # bibcodes = ['2019A&A...623A..72G', '2019A&A...623A..72G']
    links = [l for l in links if any([b in l for b in bibcodes])]
    
    # Replace '\t' with ' ' in the links
    links = [l.replace('\t', ' ') for l in links]

    # Add unnecessary link to the list to check if the regex is working
    # links = links + ['021ZNatA..76...43C /proj/ads/fulltext/sources//0076/zna-2020-0228.ocr Versita']

    # import pdb;pdb.set_trace()
    # compile regexs, they will be used in the list comp loop below
    rx_keep_prog = re.compile(rx_keep)
    rx_ignore_prog = re.compile(rx_ignore)


    # separate the XML sources, assumes the lines are all of the shape:
    # 021ZNatA..76...43C    /proj/ads/fulltext/sources//0076/zna-2020-0228.xml  Versita
    # links_filtered = [' '.join(l.split()[0:2])
    links_filtered = [' '.join(l.split())
                     for l in tqdm(links) 
                     if (rx_keep_prog.match(l) and not rx_ignore_prog.match(l))
                    ]

    return links_filtered
