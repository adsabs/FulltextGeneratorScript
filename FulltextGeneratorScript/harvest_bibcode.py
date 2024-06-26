import time
import os
import json

import requests
from adsputils import setup_logging, load_config
from urllib.parse import urlencode, quote_plus

config = load_config(proj_home=os.path.realpath(os.path.join(os.path.dirname(__file__), '../')))

def harvest_bibcode(doi, fields='bibcode'):
    ''' Harvests bibcodes for an input list of identifiers using the ADS API.

    Log in output_dir/logs/harvest_clean.log -> tail -f logs/harvest_clean.log .
    doi: input identifier to harvest bibcode for
    '''

    logger = setup_logging('harvest_clean', proj_home=os.path.dirname('harvest_log.txt'))

    logger.info('Start of harvest')

    to_log = ''

    attempts = config['SOLR_ATTEMPTS']
    successful_req = False

    while (not successful_req) and (attempts<10):
        r_json = None
        encoded_query = urlencode({"q": f'identifier:"{doi}"',
                                   "fl": fields,
                                   "rows": 1
                                  })

        r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?{}".format(encoded_query), \
                                   headers={'Authorization': 'Bearer ' + config['API_TOKEN']}
                                )
        if r.status_code==200:
            successful_req=True
        else:
            to_log += 'REQUEST {} FAILED: CODE {}\n'.format(attempts, r.status_code)
            to_log += str(r.text)+'\n'

        attempts+=1
        time.sleep(attempt + 0.5)

    if successful_req:
        r_json = r.json()
        try:
            bibcode = r_json['response']['docs'][0]['bibcode']
        except:
            bibcode = None


        to_log += 'Harvested bibcode for {}\n'.format(doi)


    else:
        to_log += 'FAILING DOI: {}\n'.format(doi)
        bibcode = None

    logger.info(to_log)

    return bibcode
