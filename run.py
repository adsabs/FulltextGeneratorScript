#!/usr/bin/env python
"""
"""

# __author__ = 'tsa'
# __maintainer__ = 'tsa'
# __copyright__ = 'Copyright 2024'
# __version__ = '1.0'
# __email__ = 'ads@cfa.harvard.edu'
# __status__ = 'Development'
# __credit__ = ['T. Allen']
# __license__ = 'MIT'

import os
import csv
import shutil
import argparse
from pathlib import Path


from OpenCorpusScript.extract_plain_text import extract_plain_text
from OpenCorpusScript.harvest_bibcode import harvest_bibcode
from OpenCorpusScript.extract_all_links import extract_all_links

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

def create_output_directory(output_directory):

    output_directory_path = Path(output_directory)

    # First delete directory if it exists
    if output_directory_path.exists():
        print('Output directory exists, deleting')
        shutil.rmtree(output_directory_path)

    # Now create the new directory
    output_directory_path.mkdir(parents=True, exist_ok=True)

    return output_directory_path

# =============================== MAIN ======================================= #
                                                                                
# To test the classifier                                                        
# For plain text
# python run.py -b OpenCorpus/tests/stub_data/stub_bibcodes_doi.txt
# For XML
# python run.py -b OpenCorpus/tests/stub_data/stub_bibcodes_doi.txt -x
                                                                                
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

    # Creata a fail list
    fail_list = []
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
            if bibcode is None:
                fail_list.append(source_id)

    # Write the fail list to a file
    with open(output_directory+'/failed_ids.txt','w') as f:
        for line in fail_list:
            f.write(f"{line}\n")

    # Create directories for plain text and source text
    # Note one or both may be used
    plain_text_directory = create_output_directory(output_directory+'/plain_text/')
    source_text_directory = create_output_directory(output_directory+'/xml_text/')

    # Create list of mapping from input ID to output file
    mapping_list = []

    # Create mapping file
    mapping_batch = 500 # batch size for writing to the mapping file
    mapping_file = output_directory + "/mapping_file.txt"
    with open(mapping_file,'w') as f:
        f.write('Identifier Filename\n')

    # Extract the plain text for the bibcodes
    # Loop through the source_list list defined above, 
    for index, item in enumerate(source_list):
        # Loop through records and extract relevant text
        # import pdb;pdb.set_trace()
        mapping_line = None  

        # Case where we are extracting plain text
        if not args.extract_xml:
            print("Extracting Plain Text")
            if item['source_info'] is not None:
                bibcode = item['source_info']['source_bibcode']
                output_filename = item['source_info']['source_filename']
                output_filename = output_filename.split('.')
                output_filepath = output_filename[0]
                output_filename = output_filename[0] + '.txt'

                # Copy the plain text to local directory
                # Note this will copy fulltext.txt.gz, acknowledgments.txt.gz and meta.json 
                # to a directory named output_filepath
                extract_success = extract_plain_text(bibcode, output_filepath, plain_text_directory)

                # Write filename mapping to file
                mapping_path = f"{plain_text_directory}/{output_filepath}".split('/')[-2:]
                mapping_path = '/'.join(mapping_path)
                mapping_line = f"{item['source_id']} {mapping_path}\n"
                mapping_list.append(mapping_line)

        # Case where we are extracting from all.links source or fulltext not availible
        if args.extract_xml or extract_success is False:
            # Extract source
            if item['source_info'] is not None:
                
                src = item['source_info']['source_path']
                dest = f"{source_text_directory}/{item['source_info']['source_filename']}"
                try:
                    # shutil.copyfile(src, dest)
                    shutil.copy(src, dest)
                    print(f"Copied source text for : {item['source_id']}")
                    with open(plain_text_directory/"mapping_file.txt",'a') as f:
                        f.write(f"{item['source_id']} {item['source_info']['source_filename']}\n")
                except:
                    print(f"Source text for bibcode: {item['source_id']} not found")
                mapping_path = f"{source_text_directory}/{item['source_info']['source_filename']}".split('/')[-2:]
                mapping_path = '/'.join(mapping_path)
                mapping_line = f"{item['source_id']} {mapping_path}\n"
                mapping_list.append(mapping_line)

        # Write mapping list to file
        # Do so for every 500 records
        if (index + 1 % mapping_batch) == 0 or (index == len(source_list)-1):
            with open(mapping_file, 'a') as f:
                for line in mapping_list:
                    f.write(line)
            # Reset mapping_list to an empty list
            mapping_list = []
                                                                                
    print("Done")                                                               
