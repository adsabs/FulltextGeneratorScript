import os
import re
import shutil
import gzip

import ptree
from tqdm.auto import tqdm

# This scripts extracts the full text for all articles that ADS has open access
# availablility.

def extract_plain_text(bibcode, output_filename, output_directory):

    # base path for fulltext files
    # base_path = "/proj/adsnull/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"
    base_path = "/proj/adsnest/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"

    # Loop through all bibcodes in list
    fulltext_path = None
    print()
    print(bibcode)

    # Add path to full text to dataframe for each article
    text_path = os.path.join(base_path, ptree.id2ptree(bibcode))

    # Replace periods in bibcode with commas
    #         ampersands         with and
    # bibcode_filename = bibcode.replace('.', ',')
    # bibcode_filename = bibcode_filename.replace('&', 'and')

    # Copy the plain text to a local directory
    try:
        # Will copy the whole directory - including fulltext, acknowledgements
        # and metadata 
        # shutil.copytree(base_path+text_path, output_directory)
        # Will copy just the plain text file
        src = base_path+text_path+'fulltext.txt.gz'
        dest = output_directory / 'fulltext.txt.gz'
        dest_unzipped = output_directory / output_filename
        # shutil.copyfile(src, dest)
        shutil.copy(src, dest)
        print(f"Copied bibcode: {bibcode})")
        # Now unzip the plaintext file locally and rename the output
        with gzip.open(dest, 'rb') as infile:
            with open(dest_unzipped, 'wb') as outfile:
                for line in infile:
                    outfile.write(line)
        success = True
    except:
        print(f"Plain text for bibcode: {bibcode} not found")
        success = False

    # import pdb;pdb.set_trace()
    return success

         



