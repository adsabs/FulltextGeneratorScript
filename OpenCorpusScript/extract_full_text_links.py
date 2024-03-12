import os
import re

import pandas as pd
import ptree
from tqdm.auto import tqdm

# This scripts extracts the full text for all articles that ADS has open access
# availablility.


if __name__ == "__main__":


    # Input dataframe with open access articles
    data_path = "data/open_corpus_records.csv"
    out_path = 'data/open_corpus_records_paths.csv'

    df = pd.read_csv(data_path)

    # File with path to all the .ocr and .xml fulltext files
    # This file also contains the source of the fulltext, i.e. ADS,
    # arXiv, IOP, Elsevier, etc.
    # Note that this file was copied from
    # /proj/ads/abstracts/config/links/fulltext/all.links 
    # to the local data/ directory on 06/23/23.
    link_file = 'data/all.links'

    df_links = pd.read_table(link_file,sep='\t', names= ['bibcode', 'path', 'access'])

    # Before merging the all.links file with the results of the solr query, 
    # obtain a list of the possible bibstems used for arXiv papers.
    df_arxiv = df_links[df_links['access']=='arXiv']

    # each path variable has the form:
    # /proj/ads/abstracts/sources/ArXiv/fulltext/arXiv/1002/1810.pdf
    # We want the directory after /fulltext/. Hopefully isolating
    # these gives the full range of possible values for arxiv papers
    df_arxiv['sub_field'] = df_arxiv['path'].apply(lambda x: x.split('/')[7])

    arxiv_vals = df_arxiv['sub_field'].unique()

    # Note that the list created above does not translate directly
    # into bibstems for arxiv access articles, For instance
    # cond-mat is co.mat
    # chao-dyn is chao.dyn

    # The following list of arxiv bibstems was curated from 
    # an older version of the dataset
    # data/open_corpus_final_references_for_arxiv_bibstems.csv

    with open("data/bibstems_unique_arxiv_edited.txt", "r") as f:
        arxiv_bibstems = f.readlines()

    arxiv_bibstems = [line.rstrip('\n') for line in arxiv_bibstems]

    # Make a regex out of the list of arXiv bibstems

    arxiv_regex = '|'.join(arxiv_bibstems)
    arxiv_regex = arxiv_regex.replace('.','\.')
    # ar = str(arxiv_regex)
    # import pdb;pdb.set_trace()
    # arxiv_regex = '^(?!.*[:/-])' + ar + '$'
    # arxiv_regex = '^(?!.*[/])' + ar + '$'

    # Patterns to avoid when determining arXiv bibstems
    avoid_regex = '/|book|conf|work|rept|csss|conv'

    # import pdb;pdb.set_trace()


    df = pd.merge(df, df_links, on='bibcode', how='left')

    # make sure thare are no NaN's in the list of fulltext sources
    # This may happen if the all.links fule that is used is newer
    # (and thus has more files in it) that the query of accessible
    # fulltext articles
    df = df.dropna(subset=['access'])

    # Get a  list of the unique sources of fulltext 

    fulltext_sources = df['access'].unique()

    # Sources of fulltext that are not ADS or arXiv
    # this is the variable fulltext_sources with 'ADS' and 'arXiv' removed
    # This a hand curated list - the 'ADS' and 'arXiv' sources were removed

    publishers = ['IOP', 'Elsevier', 'Springer', 'APS', 'AIP', 'OUP',
                     'PHAEDRA', 'SPRINGER', 'EGU', 'SAGE', 'Wiley', 'EDP', 'NATURE',
                     'AnRev', 'Versita', 'ASJ', 'CUP', 'RSOC', 'Natur', 'AN', 'POS',
                     'AGU', 'AsBio', 'SPIE', 'AAA', 'JAHH', 'LPI', 'AMS', 'ZENODO',
                     'SARA', 'JACoW']

    # Use to test some paths that are not being correctly 
    # identified
    # df = pd.read_csv('data/dataset_bad_paths.csv')
    # df = df.iloc[1:3, :]

    # import pdb;pdb.set_trace()

    df['bibcode_path'] = None
    df['arxiv_bibcode'] = None
    df['arxiv_path'] = None
    df['fulltext_bibcode'] = None
    df['fulltext_path'] = None

    

    # base path for fulltext files
    base_path = "/proj/adsnull/docker/volumes/backoffice_prod_fulltext_pipeline_live/_data/"

    # Loop through all articles in dataset
    # for index, row in tqdm(df.iterrows(), total=df.shape[0]):
    for index, row in df.iterrows():
    # for index, row in df.iterrows():
        fulltext_path = None
        print()
        print(index)
        print(row['bibcode'])
        print(row['identifier'])
        print(row['access'])
        tmp_arxiv_bibcode = None

        # import pdb;pdb.set_trace()
        
        # Add path to full text to dataframe for each article
        df.at[index, 'bibcode_path'] = os.path.join(base_path, ptree.id2ptree(row['bibcode']))


         
        # Use the dafault path for anything that has ADS or arXiv acceess
        # if (row['access']=='ADS' or row['access']=='arXiv'): 
        # if row['access']=='ADS': 
        # if row['ads_openaccess'] is True:
        if (row['ads_openaccess'] is True and row['access']=='ADS'):

            df.at[index,'fulltext_path'] = os.path.join(base_path, ptree.id2ptree(row['bibcode']))
            df.at[index,'fulltext_bibcode'] = row['bibcode']
            print()
            print("ADS or arXiv")
            print(row['bibcode'])
            print(row['access'])
    
        # Check if the fulltext is from a publisher
        # elif row['access'] in publishers:
        # elif (row['access'] in publishers or row['access']=='arXiv'):
        elif (row['ads_openaccess'] is False) or (row['ads_openaccess'] is True and row['access']!='ADS'):
            print()
            print('Access From Publisher')
            print(row['bibcode'])
            print(row['access'])

            # res = [ele for ele in arxiv_bibstems if(ele in arxiv_bibstems)]
            # Search through list of arXiv bibstems to find arXiv bibcode
            # and use as fulltext_path
            print('Identifiers')
            valid_id = []
            for element in eval(row['identifier']):
                # print(element)
                # print(len(element))
                if len(element) == 19 and re.search(arxiv_regex, element):
                    # arxiv_article = element
                    print(element)
                    print(len(element))
                    valid_id.append(element)
                    print('Search results')
                    print(re.search(arxiv_regex, element))
                    # print('arXiv bibcode')
                    # df.at[index,'arxiv_bibcode'] = element
                    # df.at[index,'fulltext_bibcode'] = element
                    # df.at[index,'arxiv_path'] = os.path.join(base_path, ptree.id2ptree(element))
                    # df.at[index,'fulltext_path'] = os.path.join(base_path, ptree.id2ptree(element))
            print('Valid Elements')
            print(valid_id)
            for element in valid_id:
                if not re.search(avoid_regex, element):
                    print('arXiv bibcode')
                    print(element)
                    df.at[index,'arxiv_bibcode'] = element
                    df.at[index,'fulltext_bibcode'] = element
                    df.at[index,'arxiv_path'] = os.path.join(base_path, ptree.id2ptree(element))
                    df.at[index,'fulltext_path'] = os.path.join(base_path, ptree.id2ptree(element))
            # res = [x for x in arxiv_vals if(x in row['identifier'])]
            # if index == 199:
            #     import pdb;pdb.set_trace()

            # print('Arxiv bibcode')
            # print(arxiv_article)

            




        # Old Version
        """
        df.at[index, 'bibcode_path'] = os.path.join(base_path, ptree.id2ptree(row['bibcode']))
        # Identify if there is an ArXiv version of an article by searching
        # through the list of alternate identifiers,  Note not all ArXiv
        # articles have arxiv in thier name, some may have the subject matter
        # instead, i.e. co.mat.  This searches for identifiers that are the
        # length of a bibcode (19 characters) and the relevant characters
        # for the journal (4-8) are different than the base bibcode.  
        for identifier in eval(row['identifier']):
            if len(identifier)==19 and identifier[4:8]!=row['bibcode'][4:8]:
                tmp_arxiv_bibcode = identifier

        # If ADS does not have open access use the path to the 
        # ArXiv version of the paper
        if tmp_arxiv_bibcode and row['access'] != "ADS":
            print('arXiv bibcode')
            print(tmp_arxiv_bibcode)
            df.at[index, 'arxiv_bibcode'] = tmp_arxiv_bibcode
            df.at[index, 'arxiv_path'] = os.path.join(base_path, ptree.id2ptree(tmp_arxiv_bibcode))

            fulltext_path = os.path.join(base_path, ptree.id2ptree(tmp_arxiv_bibcode))
            df.at[index, 'fulltext_path'] = fulltext_path
        # Otherwise use the path to the full text of the actual article
        else:
            fulltext_path = os.path.join(base_path, ptree.id2ptree(row['bibcode']))
            df.at[index, 'fulltext_path'] = fulltext_path

        print("fulltext path:")
        print(fulltext_path)
        """

    # Choose the columns we want to save
    print('Cleaning the dataset')
    df = df[['bibcode', 'identifier', 'astronomy', 'ads_openaccess','eprint_openaccess', 'path', 'access', 'bibcode_path', 'arxiv_bibcode','arxiv_path', 'fulltext_bibcode', 'fulltext_path']]

    # Add one more column that consolidtes 'ads_openaccess' and 'arxiv_openacess'
    # into one column
    df['open_access'] = None

    for index, row in df.iterrows():
        if row['ads_openaccess'] is True and row['eprint_openaccess'] is True:
            df.at[index, 'open_access'] = 'ADS and arXiv'
        elif row['ads_openaccess'] is True and row['eprint_openaccess'] is False:
            df.at[index, 'open_access'] = 'ADS'

        elif row['eprint_openaccess'] is True and row['ads_openaccess'] is False:
            df.at[index, 'open_access'] = 'arXiv'

        else:
            df.at[index, 'open_access'] = 'other'

    # Now add a column for bistems
    # Remove last character from bibcode - It typically is a letter
    df['bibstem'] = df['fulltext_bibcode'].apply(lambda x: str(x)[:-1])

    # Now remove all digits from bibcodes to get th bibstem
    pattern_digits = r'[0-9]'
    df['bibstem'] = df['bibstem'].apply(lambda x: re.sub(pattern_digits, '', x).rstrip('.'))
    # pattern_periods = r'\\.+*'
    #

    df.to_csv(out_path, index=False)
