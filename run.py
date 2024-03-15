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

from OpenCorpusScript.extract_xml_links import extract_xml_links
from OpenCorpusScript.extract_plain_text import extract_plain_text
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
                                                                                
    parser.add_argument('-b',                                                   
                        '--bibcodes',                                        
                        dest='bibcodes',                                     
                        action='store',                                    
                        help='Path to text file with list of bibcodes to extract full text')                             
                                                                                
    parser.add_argument('-x',                                                   
                        '--xml',                                           
                        dest='extract_xml',
                        action='store_true',
                        help='Set to extract XML insted of plain text')
                                                                                
                                                                                
    args = parser.parse_args()                                                  

                                                                                
                                                                                
    if args.bibcodes:                                                            
        bibcodes_path = args.bibcodes
        print(bibcodes_path)                                                     
        
        # Read the bibcodes file and extract the bibcodes into a list
        with open(bibcodes_path, 'r') as f:                                      
            # bibcodes = f.readlines()
            bibcodes = f.read().splitlines()

        # For now let the output directory be the same directory as the input file
        output_directory = os.path.join(*bibcodes_path.split("/")[0:-1])
        

    # all.links path on server is /proj/ads/abstracts/links/all.links
    # First copy all.links locally 
    # Will need to mount the propoer volume
    # all_links_path = '/proj/ads/abstracts/links/all.links'  
    # will use local copy for testing
    all_links_path = 'OpenCorpusScript/tests/stub_data/all.links'

    # shutil.copyfile(all_links_path, all_links_path_local)
    # import pdb;pdb.set_trace()


    # Case where we are extracting plain text
    if not args.extract_xml:
        print("Extracting Plain Text")
        # Extract the plain text for the bibcodes
        # This will be a separate function
        # The function will take the bibcodes and the path to the all.links file
        # It will return a list of plain text strings
        # For now, we will just print the bibcodes
        print(bibcodes)
        print(all_links_path)
        plain_text_list = extract_plain_text(bibcodes, output_directory+'/plain_text')
        print("Done Extracting Plain Text Links")
        # import pdb;pdb.set_trace()

    # Case where we are extracting XML
    if args.extract_xml:
        print("Extracting XML")
        # Extract the XML for the bibcodes
        # This will be a separate function
        # The function will take the bibcodes and the path to the all.links file
        # It will return a list of XML strings
        # For now, we will just print the bibcodes
        print(bibcodes)
        print(all_links_path)

        xml_list = extract_xml_links(bibcodes, all_links_path, output_directory)
        print("Done Extracting XML Links")
        import pdb;pdb.set_trace()

                                                                                
                                                                                
    print("Done")                                                               
    import pdb;pdb.set_trace()           
