from msrest.authentication import CognitiveServicesCredentials
from config import DefaultConfig
import pandas as pd

import json, requests


class CogSearchHelper:

    def __init__(self):
        """
        Connects to cognitive services and stores results from search term.

        :param self.results: information found during search
        :type self.results: object
        """
        config = DefaultConfig

        self.__runtime_key = config.COG_SEARCH_KEY
        self.__runtime_endpoint = config.COG_SEARCH_HOST_NAME
        self.__runtime_version = config.COG_SEARCH_VERSION
        self.__runtime_index = f'indexes/{config.COG_SEARCH_INDEX}/docs'
        self.__headers = {'Content-Type': 'application/json',
                         'api-key': self.__runtime_key}
        self.results = pd.DataFrame()

    def search_staging_docs(self, term: str, role: str) -> bool:
        """
        Uses cognitive search to find items with terms.

        :param term: term to search for
        :type term: str
        :param role: role to determine which field should be searched
        :type role: str
        :return: Are there documents found?
        :rtype: bool
        """

        self.results = self.results.iloc[0:0]

        # TODO: make more generic so the type of search is passed through as well as the
        #       terms.  e.g. do we want to filter, search, by what field etc.  Have to
        #       make this be flexible for any document search. Ideas:
        #       Search term: str
        #       Filter term: str  Filter field: str
        #       Weighting to use: str
        #       pass in dataframe and iterate??


        print(f'Search: {role}, {term}')

        url = self.__runtime_endpoint + self.__runtime_index + "?api-version=" + self.__runtime_version

        # TODO: make this a seperate method to build up url based on params passed in!
        if role == 'subject':
            url += "&search=" + term
        elif role == 'task':
            url += f"&search=*&%24filter=tasks%20eq%20'{term}'"

        response = requests.get(url, headers=self.__headers)
        index_list = response.json()

        df = pd.json_normalize(index_list['value'])
        self.results = self.results.append(df, ignore_index=True)

        if not self.results.empty:
            return True
        else:
            return False
