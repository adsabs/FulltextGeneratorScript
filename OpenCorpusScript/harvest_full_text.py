import os
import shutil
import math

import pandas as pd
import ptree
from tqdm.auto import tqdm

# This script copies the full text of the open access articles
# into one local directory.

def harvest_plain_text(bibcodes):
    """
    Harvest plain text for specified bibcodes

    Args:

    bibcodes: list of bibcodes

    Returns:

    None

    """

    # in_data_path = "data/open_corpus_records_paths.csv"
    # out_data_path = "data/fulltext/"
    # out_df_path = "data/open_corpus_records_paths_fulltext_source.csv"


    # df = pd.read_csv(in_data_path)


    # base_path = "/proj/adsnest/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"
    # # base_path = "/proj/adsnull/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data"
    # dest_base = "data/fulltext"

    # print(df.columns)
    # df['status'] = None

    # copy_file = True # Set to False to debug

    # Loop through data and copy full tet from server to local directory
    for index, row in df.iterrows():
        print()
        print(index)
        print(row['bibcode'])
        dir_path = None
        dest_path = None

        dir_path = row['fulltext_path']
        dest_path = row['bibcode_path']
        if type(row['fulltext_path']) is float:
            print("No fulltext path available")
            df.at[index, 'status'] = "Not Available"
            continue
            # import pdb;pdb.set_trace()

        # if index==1609:
        #     import pdb;pdb.set_trace()
        full_path = base_path + dir_path
        dest_path = dest_base + dest_path

        print("Source Path")
        print(full_path)
        print("Dest Path")
        print(dest_path)
        # Copy full text to local directory
        # If full text is not available, add a flag in the data table
        if copy_file:
            try:
                shutil.copytree(full_path, dest_path)
                df.at[index, 'status'] = "Available"
            except:
                print("File not Found")
                df.at[index, 'status'] = "Not Available"

    
    df.to_csv(out_df_path, index=False)

