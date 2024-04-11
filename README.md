# OpenCorpusScript
This code can be used to generate a fulltext dataset using either plaintext files or source (i.e. XML, Latex, pdf) files from the SciX corpus.


## To operate

The script requires a text file with a list of identifiers (can be bibcodes, dois, etc.) for the papers of interest.  

For plain text output simply pass the path for the text file to the script using the `-i` or `--input` flag.

`>python3 generate_fulltext_extraction.py -i OpenCorpusScript/tests/stub_data/stub_bibcodes_doi.txt`

If the prefered output is the source file, i.e., XML, pdf or LaTeX , simply add the `-s` or `--source` flag.

`>python3 generate_fulltext_extraction.py -i OpenCorpusScript/tests/stub_data/stub_bibcodes_doi.txt -s`
