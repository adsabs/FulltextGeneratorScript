# OpenCorpus

This code is used to compile and curate the Open Corpus dataset.  The Open Corpus dataset is a dataset of ~2.8 million full text articles from ADS that are open access.  The articles are primarily astrophysics, and includes non-atrophysics articles cited by the astrophysics literature.


## Output

The final dataset is composed of a `.csv` file and a data directory. The data directory contains the fulltext of the articles in the dataset.  The `.csv` file, called `open_corpus_NASA.csv', contains the following columns: 
* bibcode - A unique reference for each article in the dataset,
* path - The path to the fulltext of the article within the data directory. This path is composed of the bibcode of the article in a hierarchy of directories where each directory contains two characters from the bibcode.  Further all periods in the bibcodes are replaced with commas in the path.  For example, the bibcode `2019ApJ...887..105C` would have the path `20/19/Ap/J,/,,/88/7,/,1/05/C`.
* language - The primary language of the article.
* references - A list of bibcodes for articles that a record article referes to.
* citations - A list of bibcodes for articles that cite the record article..

To open using Python and Pandas:

```
import pandas as pd

df = pd.read_csv('open_corpus_NASA.csv')

for index, row in df.iterrows():
    f=gzip.open('data/fulltext' + {row['path'],'rb')
    file_content=f.read()
```

Note: then fulltext_path column gives the path to the full text article within the `fulltext` directory.

### Abstracts

A dataset is also created that contains all available abstracts for the
 Open Corpus records.  This dataset called `open_corpus_ABSTRACTS.csv`, contains
 information about the abstract (located `'data/abstracts/' + row['path']` for each record)

```
import pandas as pd

df = pd.read_csv('open_corpus_ABSTRACTS.csv')

for index, row in df.iterrows():

    with open('data/abstracts' + row['path'], 'r') as f:
        file_content=f.read()
```

## Usage

The `bash` script `run_OpenCorpus.sh` contains the python scripts in the appropriate order.
To create the dataset the following scripts should be run in the given order.

* `query_data.py`: This script queries SOLR to find articles that either ADS has open access to the full text or ADS has an ArXiv version of the full text. Saves output as `open_corpus_records.csv`.

* `extract_full_text_links.py`: This script takes the output from the SOLR query and extracts the links to the fulltext version of the article.  Saves output as `open_corpus_records_paths.csv`

* `harvest_full_text.py`: This script takes the `open_corpus_records_paths.csv` file and copies the fulltext to a local directory `data/fulltext/`.  It saves the outpus as `open_corpus_records_paths_fulltext_source.csv`.

* `run_harvest_solr_references_abstracts.py`: Wraps the function in `harvest_solr_references_abstracts.py` to query the ADS API for each bibcode in `open_corpus_records_paths_fulltext_source.csv` and returns a list of references, citations and abstract, if available, for each article.  Note: that the ADS API rate limit had to be increased to 2000 queries in a day to allow the script to run in a reasonable amount of time.  

* `label_available_abstracts.py`: Takes `open_corpus_final_references.csv` as an input and appends a column called `abstract_status` that takes the values `'Available'` if the abstract exists or `'Not Available'` if the abstract does not exist.  Saves the resulting table as `open_corpus_records_paths_fulltext_source_abstracts.csv`.

* `compile_bibcodes_references.py`: This script aggregates all the JSON files that hols the references for articles into one dataframe and joins them to the dataset. Takes `open_corpus_records_paths_fulltext_source.csv` as input and creates the dataset `open_courpus_record_paths_fulltext_source_abstracts.csv`.

* `detect_language.py`: Uses `pycld2` to detect the prominent language of the fulltext.  Saves output as `open_corpus_records_paths_fulltext_source_abstracts_references_citations_ft_language.csv`.

* `detect_language_abstracts.py`: Uses `pycld2` to detect the prominent language of the abstract.  Saves output as `open_corpus_records_paths_fulltext_source_abstracts_references_citations_ft_language_abs_language.csv`.

* `clean_final_dataset.py`: This takes `open_courpus_final_references_citations.csv` and removes all columns except four contained in the final dataset.  Saves output as `open_corpus_NASA.csv`, `open_corpus_ABSTRACTS.csv`, `open_corpus_ADS.csv` or `open_corpus_ADS_no_vectors.csv`


