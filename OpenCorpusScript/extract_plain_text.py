import os
import re
import shutil
import gzip

import ptree
from tqdm.auto import tqdm

# This scripts extracts the full text for all articles that ADS has open access
# availablility.

def extract_plain_text(bibcode, output_filepath, output_directory, unzip_text=True):
    """ Copy fulltext, acknowledgements and meta.json from stroage on server to 
        local directory

        bibcode: bibcode of record to copy
        output_filepath: name of directory to hold just a single record
        output_directory: local directory to store all records
        unzip_text: switch to unzip the files that are copied. defaults to True
    """

    # base path for fulltext files
    # base_path = "/proj/adsnull/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"
    base_path = "/proj/adsnest/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"


    # Add path to full text to dataframe for each article
    text_path = os.path.join(base_path, ptree.id2ptree(bibcode))

    # Copy the plain text to a local directory
    src = base_path+text_path
    dest = output_directory / output_filepath
    try:
        # Will copy the whole directory - including fulltext, acknowledgements
        # and metadata 
        shutil.copytree(src, dest)
        print(f"Copied bibcode: {bibcode})")
        success = True
    except:
        print(f"Plain text for bibcode: {bibcode} not found")
        success = False

    # Now if copied successfully unzip both acknowledgments.txt.gz and fulltext.gx
    if success is True and unzip_text is True:

        # First fulltext 
        try:
            unzip_dest(dest / 'fulltext.txt')
        except:
            print(f'Failed to unzip {dest}/fulltext.txt.gz')
        # Now Acknowledgments
        try:
            unzip_dest(dest / 'acknowledgements.txt')
        except:
            print(f'Failed to unzip {dest}/acknowledgements.txt.gz')

    return success

         

def unzip_dest(filename):
    '''Unzip a .gz file and write as plain text.

        filname: PosizPath to file to unzip into, should be same as zipped
                 file except without .gz at the end
    '''

    filename = str(filename)
    with gzip.open(filename +'.gz', 'rb') as infile:
        with open(filename, 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    # Now remove zipped file
    os.remove(filename + '.gz')

