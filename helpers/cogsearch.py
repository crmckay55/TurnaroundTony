from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import pandas as pd

import json, requests


class CogSearchHelper:
    """connects to congitive services and stores results from search term
    :param results: datafame of results with url, title, keywords, description, tasks, RowKey, and @search.score
    :type results: pandas dataframe
    """

    def __init__(self):
        config = DefaultConfig

        self._runtime_key = config.COG_SEARCH_KEY
        self._runtime_endpoint = config.COG_SEARCH_HOST_NAME
        self._runtime_version = config.COG_SEARCH_VERSION
        self._runtime_index = config.COG_SEARCH_INDEX
        self._headers = {'Content-Type': 'application/json',
                         'api-key': self._runtime_key}
        self.results = pd.DataFrame()

    def search(self, term: str):
        """Uses cognitive search to find items with terms
        :param term: term to search for
        :type term: str
        """

        found_docs = False
        df = pd.DataFrame()

        print('Search Terms')
        print(term)

        url = self._runtime_endpoint + self._runtime_index + "?api-version=" \
              + self._runtime_version + "&search=" + term

        response = requests.get(url, headers=self._headers)
        index_list = response.json()
        print(index_list)

        df = pd.json_normalize(index_list['value'])
        self.results = self.results.append(df, ignore_index=True)
        if len(self.results) > 0:
            found_docs = True

        # TODO: seperate searching for task number vs. subject

        return found_docs
