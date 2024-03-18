#!/usr/bin/env python
"""
"""

# __author__ = 'rca'
# __maintainer__ = 'rca'
# __copyright__ = 'Copyright 2015'
# __version__ = '1.0'
# __email__ = 'ads@cfa.harvard.edu'
# __status__ = 'Production'
# __credit__ = ['J. Elliott']
# __license__ = 'MIT'

import os
import csv
import shutil
# import sys
# import time
# import json
import argparse
# import logging
# import traceback
# import warnings
# from urllib3 import exceptions
# warnings.simplefilter('ignore', exceptions.InsecurePlatformWarning)

# import pandas as pd
# from transformers import AutoTokenizer, AutoModelForSequenceClassification

# from OpenCorpusScript.extract_xml_links import extract_xml_links
from OpenCorpusScript.extract_source_file import extract_source_file
from OpenCorpusScript.extract_plain_text import extract_plain_text
from OpenCorpusScript.harvest_bibcode import harvest_bibcode
from OpenCorpusScript.extract_all_links import extract_all_links
# from adsputils import get_date
# from adsmsg import OrcidClaims
# from SciX_Classifier import classifier, tasks
# from ADSOrcid import updater, tasks
# from ADSOrcid.models import ClaimsLog, KeyValue, Records, AuthorInfo

# # ============================= INITIALIZATION ==================================== #

from adsputils import setup_logging, load_config
proj_home = os.path.realpath(os.path.dirname(__file__))
global config
config = load_config(proj_home=proj_home)
# logger = setup_logging('run.py', proj_home=proj_home,
#                         level=config.get('LOGGING_LEVEL', 'INFO'),
#                         attach_stdout=config.get('LOG_STDOUT', False))

# app = tasks.app

# =============================== FUNCTIONS ======================================= #



# =============================== MAIN ======================================= #
                                                                                
# To test the classifier                                                        
# For plain text
# python run.py -b OpenCorpus/tests/stub_data/stub_bibcodes.txt
# For XML
# python run.py -b OpenCorpus/tests/stub_data/stub_bibcodes.txt -x
                                                                                
if __name__ == '__main__':                                                      
                                                                                
    parser = argparse.ArgumentParser(description='Process user input.')         
                                                                                
    parser.add_argument('-i',                                                   
                        '--input_ids',                                        
                        dest='input_ids',                                     
                        action='store',                                    
                        help='Path to text file with list of bibcodes or dois to extract full text')                             
                                                                                
    parser.add_argument('-x',                                                   
                        '--xml',                                           
                        dest='extract_xml',
                        action='store_true',
                        help='Set to extract XML insted of plain text')
                                                                                
                                                                                
    args = parser.parse_args()                                                  

                                                                                
                                                                                
    if args.input_ids:
        input_ids_path = args.input_ids
        print(input_ids_path)                                                     
        
        # Read the bibcodes file and extract the bibcodes into a list
        with open(input_ids_path, 'r') as f:                                      
            # bibcodes = f.readlines()
            id_list = f.read().splitlines()

        # For now let the output directory be the same directory as the input file
        output_directory = os.path.join(*input_ids_path.split("/")[0:-1])
        

    # all.links path on server is /proj/ads/abstracts/links/all.links
    # First copy all.links locally 
    # Will need to mount the propoer volume
    # all_links_path = '/proj/ads/abstracts/links/all.links'  
    # will use local copy for testing
    all_links_path = 'OpenCorpusScript/tests/stub_data/all.links'

    # shutil.copyfile(all_links_path, all_links_path_local)
    # import pdb;pdb.set_trace()

    # Loop through bibcodes and check if source link exists
    source_list = []
    for source_id in id_list:

        print(f'Searching for {source_id}')
        source = extract_all_links(source_id, all_links_path)
        source_dict = {'source_id' : source_id,
                       'source_info' : source}
        source_list.append(source_dict)

    # Now loop through id's and source list and if source list is None
    # query SOLR using the ID to obtain the bicode for the record

    # for index, (in_id, item) in enumerate(zip(id_list, source_list)):
    for index, item in enumerate(source_list):

        source_id = item['source_id']
        source = item['source_info']
        # Query SOLR if source_list value is None
        if source is None:
            bibcode = harvest_bibcode(source_id)
            # If bibcode is resolved extract info from all.links
            # and update source list
            if bibcode is not None:
                source = extract_all_links(bibcode, all_links_path)
                item['source_info'] = source
                source_list[index] = item

            # import pdb;pdb.set_trace



    # import pdb;pdb.set_trace()

        # Extract the plain text for the bibcodes
        # Loop through the source_list list defined above, 
    for index, item in enumerate(source_list):
        # Loop through records and extract relevant text
        # import pdb;pdb.set_trace()

        # Case where we are extracting plain text
        if not args.extract_xml:
            print("Extracting Plain Text")
            if item['source_info'] is not None:
                bibcode = item['source_info']['source_bibcode']
                output_filename = item['source_info']['source_filename']
                output_filename = output_filename.split('.')
                output_filename = output_filename[0] + '.txt'
                # import pdb;pdb.set_trace()
                extract_success = extract_plain_text(bibcode, output_filename, output_directory+'/plain_text/')
                # Now remove the remaining zipped file
                try:
                    os.remove(f"{output_directory}/plain_text/fulltext.txt.gz")
                except OSError:
                    pass

        # Case where we are extracting from all.links source or fulltext not availible
        if args.extract_xml or extract_success is False:
            # Extract source
            if item['source_info'] is not None:
                
                src = item['source_info']['source_path']
                dest = f"{output_directory}/xml_text/{item['source_info']['source_filename']}"
                try:
                    # shutil.copyfile(src, dest)
                    shutil.copy(src, dest)
                    print(f"Copied source text for : {item['source_id']}")
                except:
                    print(f"Source text for bibcode: {item['source_id']} not found")


                                                                                
                                                                                
    print("Done")                                                               
    # import pdb;pdb.set_trace()           
