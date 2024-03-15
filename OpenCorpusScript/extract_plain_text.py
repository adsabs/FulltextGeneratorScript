import os
import re
import shutil

import ptree
from tqdm.auto import tqdm

# This scripts extracts the full text for all articles that ADS has open access
# availablility.

def extract_plain_text(bibcodes, output_directory):

    # base path for fulltext files
    # base_path = "/proj/adsnull/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"
    base_path = "/proj/adsnest/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"

    # Loop through all bibcodes in list
    for index, bibcode in enumerate(bibcodes):
        fulltext_path = None
        print()
        print(index)
        print(bibcode)

        # Add path to full text to dataframe for each article
        text_path = os.path.join(base_path, ptree.id2ptree(bibcode))

        # Replace periods in bibcode with commas
        #         ampersands         with and
        bibcode_filename = bibcode.replace('.', ',')
        bibcode_filename = bibcode_filename.replace('&', 'and')

        # Copy the plain text to a local directory
        try:
            # Will copy the whole directory - including fulltext, acknowledgements
            # and metadata 
            # shutil.copytree(base_path+text_path, output_directory)
            # Will copy just the plain text file
            src = base_path+text_path+'fulltext.txt.gz'
            dest = output_directory+bibcode_filename
            # shutil.copyfile(src, dest)
            shutil.copy(src, dest)
            print(f"Copied bibcode: {bibcode})")
        except:
            print(f"Plain text for bibcode: {bibcode} not found")

        import pdb;pdb.set_trace()

         



