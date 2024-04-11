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
import shutil
import argparse
from pathlib import Path


from OpenCorpusScript.utils import extract_plain_text
from OpenCorpusScript.utils import harvest_bibcode
from OpenCorpusScript.utils import extract_all_links

# # ============================= INITIALIZATION ==================================== #

from adsputils import setup_logging, load_config
proj_home = os.path.realpath(os.path.dirname(__file__))
config = load_config(proj_home=proj_home)

logger = setup_logging('generate_fulltext_extraction.py', proj_home=proj_home,
                        level=config.get('LOGGING_LEVEL', 'INFO'),
                        attach_stdout=config.get('LOG_STDOUT', False))

# =============================== FUNCTIONS ======================================= #

def create_output_directory(output_directory):
    """Create output directory, after deleting previously existing one if needed
    """

    output_directory_path = Path(output_directory)

    if output_directory_path.exists():
        logger.info('Output directory exists, deleting')
        shutil.rmtree(output_directory_path)

    output_directory_path.mkdir(parents=True, exist_ok=True)

    return output_directory_path

def create_mapping_line(filepath, record):
    """Combine filepath and record information to create line to append to mapping_file
    """

    mapping_path = f"{filepath}/{record['record_info']['record_filename']}".split('/')[-2:]
    mapping_path = '/'.join(mapping_path)
    mapping_line = f"{record['record_id']} {mapping_path}\n"

    return mapping_line

def generate_fulltext_extraction(input_ids_path, extract_source=False):
    """Copy fulltext from /proj/ to a local directory

        inputs:
            input_ids_path: path to text file with bibcodes
            extract_source: extract the source file instead of plaintext

        outputs:
            None

        side effects:
            saves full text in a directory based on input_ids_path
    """


    print(f'Reading bibcodes from {input_ids_path}')                                                     
    
    with open(input_ids_path, 'r') as f:                                      
        id_list = f.read().splitlines()

    output_directory = create_output_directory(os.path.join(*input_ids_path.split("/")[0:-1],'fulltext_files'))

    with open(config['ALL_LINKS_PATH'], 'r') as f:
        links = f.read().splitlines()

    plain_text_directory = create_output_directory(os.path.join(output_directory,'plain_text'))
    source_text_directory = create_output_directory(os.path.join(output_directory,'source_text'))

    record_list = []

    fail_list = []
    fail_file = os.path.join(output_directory,'failed_ids.txt')

    mapping_list = []
    mapping_batch = 500 
    mapping_file = os.path.join(output_directory,'mapping_file.txt')
    with open(mapping_file,'w') as f:
        f.write('Identifier Filename\n')


    # Check if source link exists
    for record_id in id_list:

        record = extract_all_links(record_id, links)
        record_dict = {'record_id' : record_id,
                       'record_info' : record}
        record_list.append(record_dict)


    # Obtain bibcodes if different identifiers are used
    for index, item in enumerate(record_list):

        record_id = item['record_id']
        record = item['record_info']
        mapping_line = None  

        if record is None:
            bibcode = harvest_bibcode(record_id)

            if bibcode is not None:
                record = extract_all_links(bibcode, links)
                item['record_info'] = record
                record_list[index] = item
            else:
                fail_list.append(record_id)


        if extract_source is False:
            print("Extracting Plain Text")
            if item['record_info'] is not None:
                bibcode = item['record_info']['record_bibcode']
                output_filename = item['record_info']['record_filename']
                output_filename = output_filename.split('.')
                output_filepath = output_filename[0]
                output_filename = output_filename[0] + '.txt'

                extract_success = extract_plain_text(bibcode, output_filepath, plain_text_directory)

                mapping_path = f"{plain_text_directory}/{output_filepath}".split('/')[-2:]
                mapping_path = '/'.join(mapping_path)
                mapping_line = f"{item['record_id']} {mapping_path}\n"
                mapping_list.append(mapping_line)

        # Case where we are extracting from all.links source or fulltext not availible
        if extract_source is True or extract_success is False:

            if item['record_info'] is not None:
                
                src = item['record_info']['record_path']
                dest = f"{source_text_directory}/{item['record_info']['record_filename']}"
                try:
                    shutil.copy(src, dest)
                except:
                    print(f"Source text for bibcode: {item['record_id']} not found")
                    fail_list.append(record_id)

                mapping_path = f"{source_text_directory}/{item['record_info']['record_filename']}".split('/')[-2:]
                mapping_path = '/'.join(mapping_path)
                mapping_line = f"{item['record_id']} {mapping_path}\n"
                mapping_list.append(mapping_line)

        if (index + 1 % mapping_batch) == 0 or (index == len(record_list)-1):
            with open(mapping_file, 'a') as f:
                for line in mapping_list:
                    f.write(line)

            mapping_list = []


    with open(fail_file, 'w') as f:
        for line in fail_list:
            f.write(f"{line}\n")
                                                                                
 

# =============================== MAIN ======================================= #
                                                                                
if __name__ == '__main__':                                                      
                                                                                
    parser = argparse.ArgumentParser(description='Process user input.')         
                                                                                
    parser.add_argument('-i',                                                   
                        '--input_ids',                                        
                        dest='input_ids',                                     
                        action='store',                                    
                        help='Path to text file with list of bibcodes or dois to extract full text')                             
                                                                                
    parser.add_argument('-s',                                                   
                        '--source',                                           
                        dest='extract_source',
                        action='store_true',
                        help='Set to extract source document (of all types) instead of plain text. Note source document type may include XML, pdf or LaTeX.')
                                                                                
                                                                                
    args = parser.parse_args()                                                  
                                                                                
    if args.input_ids:
        input_ids_path = args.input_ids
        
    if args.extract_source:
        extract_source = True
    else:
        extract_source = False

    generate_fulltext_extraction(input_ids_path, extract_source=extract_source)

