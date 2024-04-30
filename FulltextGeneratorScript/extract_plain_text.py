import os
import re
import shutil
import gzip

import ptree
from adsputils import load_config

# This scripts extracts the full text for all articles that ADS has open access
# availablility.
config = load_config(proj_home=os.path.realpath(os.path.join(os.path.dirname(__file__), '../')))

def extract_plain_text(bibcode, output_filepath, output_directory, unzip_text=True):
    """ Copy fulltext, acknowledgements and meta.json from stroage on server to 
        local directory

        bibcode: bibcode of record to copy
        output_filepath: name of directory to hold just a single record
        output_directory: local directory to store all records
        unzip_text: switch to unzip the files that are copied. defaults to True
    """

    src = os.path.join(config['BASE_PATH'], ptree.id2ptree(bibcode).lstrip('/'))
    dest = os.path.join(output_directory, output_filepath)
    try:
        # Will copy includes fulltext, acknowledgements, and metadata
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
            unzip_dest(os.path.join(dest, 'fulltext.txt.gz'))
        except:
            print(f'Failed to unzip {dest}/fulltext.txt.gz')
        # Now Acknowledgments
        try:
            unzip_dest(os.path.join(dest, 'acknowledgements.txt.gz'))
        except:
            print(f'Failed to unzip {dest}/acknowledgements.txt.gz')

    return success

         

def unzip_dest(filename):
    '''Unzip a .gz file and write as plain text.

        filname: PosizPath to file to unzip into, should be same as zipped
                 file except without .gz at the end
    '''

    out_filename = '.'.join(filename.split('.')[0:-1])
    with gzip.open(filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            for line in infile:
                outfile.write(line)

    # Now remove zipped file
    os.remove(filename + '.gz')

