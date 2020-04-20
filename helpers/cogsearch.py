from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import pandas as pd

import json, requests


class CogSearchHelper:
    """
    Connects to cognitive services and stores results from search term.

    :param self.results: datafame of results with url, title, keywords, description, tasks, RowKey, and @search.score
    :type results: pandas dataframe
    """

    def __init__(self):
        config = DefaultConfig

        self._runtime_key = config.COG_SEARCH_KEY
        self._runtime_endpoint = config.COG_SEARCH_HOST_NAME
        self._runtime_version = config.COG_SEARCH_VERSION
        self._runtime_index = f'indexes/{config.COG_SEARCH_INDEX}/docs'
        self._headers = {'Content-Type': 'application/json',
                         'api-key': self._runtime_key}
        self.results = pd.DataFrame()
        self.has_documents = False

    def search_staging_docs(self, term: str, role: str):
        """
        Uses cognitive search to find items with terms

        :param term: term to search for
        :type term: str
        :param role: role to determine which search string
        :type role: str
        :return self.has_results: bool if results were found
        :type self.has_results: bool
        """

        self.has_documents = False
        self.results = self.results.iloc[0:0]

        print(f'Search Term: {term}')
        print(f'Search Role: {role}')

        url = self._runtime_endpoint + self._runtime_index + "?api-version=" + self._runtime_version

        if role == 'subject':
            url += "&search=" + term
        elif role == 'task':
            url += f"&search=*&%24filter=tasks%20eq%20'{term}'"

        response = requests.get(url, headers=self._headers)
        index_list = response.json()

        df = pd.json_normalize(index_list['value'])
        self.results = self.results.append(df, ignore_index=True)

        if not self.results.empty:
            self.has_documents = True

        return self.has_documents

    def _search_tasks_only(self):
        pass

    def _search_default(self):
        pass
