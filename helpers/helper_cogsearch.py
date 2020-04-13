from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import pandas as pd

import json, requests


class CogSearchHelper:

    def __init__(self):
        config = DefaultConfig

        self.runtime_key = config.COG_SEARCH_KEY
        self.runtime_endpoint = config.COG_SEARCH_HOST_NAME
        self.runtime_version = config.COG_SEARCH_VERSION
        self.runtime_index = config.COG_SEARCH_INDEX
        self.headers = {'Content-Type': 'application/json',
                        'api-key': self.runtime_key}
        self.results = pd.DataFrame()

    def search(self, terms):
        """terms: list of terms to search for"""

        for search_term in terms:
            url = self.runtime_endpoint + self.runtime_index + "?api-version=" + self.runtime_version + "&search=" + search_term
            print(url)
            response = requests.get(url, headers=self.headers)
            index_list = response.json()
            print(index_list)

            self.results = pd.json_normalize(index_list['value'])
